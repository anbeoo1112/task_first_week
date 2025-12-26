import os
import nest_asyncio
from typing import Dict, Optional, List
from extract_thinker import (
    Process, Extractor, ImageSplitter, TextSplitter, SplittingStrategy, CompletionStrategy, LLM
)
from core.config import config
from core.classifications import CLASSIFICATION_TREE, getClassificationsList

nest_asyncio.apply()

class DocumentProcessor:
    def __init__(self, model: Optional[str] = None, 
                 strategy: CompletionStrategy = CompletionStrategy.CONCATENATE):
        config.validate()
        self._model = model or config.processing.model
        self._strategy = strategy
    
    def run(self, filePath: str) -> Dict:
        """Process document and extract information."""
        if not os.path.exists(filePath):
            return self._err("File không tồn tại")
        
        try:
            loader, vision, loaderName = config.createLoader(filePath)
            page_count = self._countPages(filePath)
            print(f"🔄 Processing: {loaderName}, vision={vision}, pages={page_count}")
            
            extractor = Extractor()
            extractor.load_document_loader(loader)
            extractor.load_llm(LLM(self._model))
            
            if page_count == 1:
                return self._extractSingle(extractor, filePath, vision, loaderName)
            
            return self._extractMultiple(filePath, vision, loaderName, page_count)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._err(str(e)[:200])
    
    def _extractSingle(self, extractor: Extractor, filePath: str, vision: bool, loaderName: str) -> Dict:
        classifications = getClassificationsList()
        result = extractor.classify(filePath, classifications, vision=vision)
        
        if not result or result.name == "Other":
            return self._ok(category="Other", loader=loaderName, vision=vision)
        
        contract = result.classification.contract if result.classification else None
        data = None
        
        if contract:
            r = extractor.extract(filePath, contract, vision=vision, completion_strategy=self._strategy)
            data = r.model_dump() if hasattr(r, 'model_dump') else r
        
        return self._ok(
            category=self._findCategory(result.name) or result.name,
            docType=result.name,
            data=data,
            confidence=getattr(result, 'confidence', None),
            loader=loaderName,
            vision=vision
        )
    
    def _extractMultiple(self, filePath: str, vision: bool, loaderName: str, page_count: int) -> Dict:
        """
        Multi-page extraction with 'Smart Page Clamping'.
        Handles cases where Splitter detects more pages than physically exist.
        """
        print("📄 Multi-page document detected. Splitting...")
        
        # 1. Create Loaders
        # Using separate loaders for split and extract ensures clean state
        split_loader, _, _ = config.createLoader(filePath)
        
        extractor = Extractor()
        extractor.load_llm(LLM(self._model))
        # Note: We will inject pages directly, so extractor loader is less critical here,
        # but good practice to set it.
        dummy_loader, _, _ = config.createLoader(filePath)
        extractor.load_document_loader(dummy_loader)
        
        proc = Process()
        proc.load_document_loader(split_loader)
        proc.add_classify_extractor([[extractor]])
        proc.load_splitter(ImageSplitter(self._model) if vision else TextSplitter(self._model))
        proc.load_file(filePath)
        
        classifications = getClassificationsList()
        for c in classifications:
            c.extractor = extractor
        
        # 2. Split
        strategy = SplittingStrategy.EAGER if page_count <= config.processing.eagerPageThreshold else SplittingStrategy.LAZY
        try:
            proc.split(classifications, strategy=strategy)
        except KeyError as e:
            if 'image' in str(e) and vision:
                print("⚠️ Fallback to TextSplitter due to missing image data.")
                proc.load_splitter(TextSplitter(self._model))
                proc.split(classifications, strategy=strategy)
            else:
                raise e
        
        groups = proc.doc_groups or []
        print(f"📊 Found {len(groups)} document group(s).")
        
        # 3. Validation & Correction (The "Eval" Step)
        # We detect hallucinations (page out of range) and fix them in-place
        self._sanitize_groups(groups, page_count)

        # 4. Extract (Standard Library Call)
        # Now that groups are sanitized, we can safely use the standard process
        print("📝 Extracting (Process.extract)...")
        
        try:
            results = proc.extract(vision=vision, completion_strategy=self._strategy)
            
            documents = []
            for group, data in zip(groups, results):
                data_dict = data.model_dump() if hasattr(data, 'model_dump') else data
                documents.append({
                    "category": self._findCategory(group.classification),
                    "docType": group.classification,
                    "data": data_dict,
                    "confidence": getattr(group, 'confidence', None),
                    "_debug": {"loader": loaderName, "vision": vision, "pages": len(group.pages)}
                })
                print(f"   ✅ Extracted: {group.classification}")
                
            return {"documents": documents, "error": None}
            
        except Exception as e:
            print(f"❌ Process.extract failed: {e}")
            import traceback
            traceback.print_exc()
            return {"documents": [], "error": f"Process Error: {str(e)}"}

    def _sanitize_groups(self, groups, max_pages: int):
        """
        Detects and fixes Splitter hallucinations (e.g. Page 3 in a 2-page doc).
        Acts as an in-place evaluator and corrector.
        """
        for group in groups:
            if not hasattr(group, 'pages') or not group.pages:
                continue
            
            original_pages = list(group.pages)
            sanitized_pages = []
            modified = False
            
            for p in group.pages:
                # 1-based index from Splitter
                if p > max_pages:
                    print(f"   ⚠️ Hallucination Detected: Group '{group.classification}' claims Page {p}, but doc has only {max_pages} pages.")
                    # Fix: Clamp to last page
                    sanitized_pages.append(max_pages)
                    modified = True
                else:
                    sanitized_pages.append(p)
            
            if modified:
                # Deduplicate while preserving order
                group.pages = list(dict.fromkeys(sanitized_pages))
                print(f"   🔧 Corrected Pages: {original_pages} -> {group.pages}")
    
    def _getContractByName(self, docTypeName: str):
        for node in CLASSIFICATION_TREE.nodes:
            if hasattr(node, 'children'):
                for child in node.children:
                    if child.name == docTypeName:
                        return child.classification.contract if child.classification else None
        return None
    
    def _findCategory(self, docTypeName: str) -> Optional[str]:
        for node in CLASSIFICATION_TREE.nodes:
            if hasattr(node, 'children'):
                for child in node.children:
                    if child.name == docTypeName:
                        return node.name
        return None
    
    def _ok(self, category=None, docType=None, data=None, confidence=None, loader="?", vision=False):
        return {"documents": [{
            "category": category, 
            "docType": docType, 
            "data": data,
            "confidence": confidence, 
            "_debug": {"loader": loader, "vision": vision}
        }], "error": None}
    
    def _err(self, msg: str):
        return {"documents": [], "error": msg}
    
    def _countPages(self, filePath: str) -> int:
        ext = os.path.splitext(filePath)[1].lower()
        if ext == '.pdf':
            try:
                import fitz
                doc = fitz.open(filePath)
                n = len(doc)
                doc.close()
                return n
            except:
                pass
        return 1

DocumentAIProcessor = DocumentProcessor
