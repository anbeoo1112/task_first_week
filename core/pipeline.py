import os
import asyncio
import nest_asyncio
from typing import Dict, Optional, List
from extract_thinker import (
    Process, Extractor, ImageSplitter, TextSplitter, SplittingStrategy, CompletionStrategy,
    DocumentLoaderPyPdf, DocumentLoaderSpreadSheet, DocumentLoaderGoogleDocumentAI, GoogleDocAIConfig, LLM
)
from core.config import config
from core.classifications import CLASSIFICATION_TREE, getContractForDocType, getClassificationsList

# Fix for Streamlit async issue - allow nested event loops
nest_asyncio.apply()

EXCEL_EXT = {'.xlsx', '.xls', '.xlsm', '.xlsb', '.ods'}


class DocumentProcessor:
    def __init__(self, model: Optional[str] = None, 
                 strategy: CompletionStrategy = CompletionStrategy.CONCATENATE):
        config.validate()
        self._model = model or config.processing.model
        self._strategy = strategy
    
    def run(self, filePath: str) -> Dict:
        if not os.path.exists(filePath):
            return self._err("File không tồn tại")
        
        try:
            ext = os.path.splitext(filePath)[1].lower()
            
            # Choose loader and vision mode
            if config.ocr.isImageFile(filePath) or (ext == '.pdf' and not self._hasText(filePath)):
                loader = self._docaiLoader()
                vision = True
                loaderName = "docai"
            elif ext in EXCEL_EXT:
                loader = DocumentLoaderSpreadSheet()
                vision = False
                loaderName = "spreadsheet"
            else:
                loader = DocumentLoaderPyPdf()
                vision = False
                loaderName = "pypdf"
            
            print(f"🔄 Using {loaderName}, vision={vision}")
            
            # Create extractor
            extractor = Extractor()
            extractor.load_document_loader(loader)
            extractor.load_llm(LLM(self._model))
            
            # Create Process
            proc = Process()
            proc.load_document_loader(loader)
            proc.add_classify_extractor([[extractor]])
            proc.load_splitter(ImageSplitter(self._model) if vision else TextSplitter(self._model))
            proc.load_file(filePath)
            
            # SPLIT first to detect multiple documents!
            print("🔍 Splitting document...")
            # Convert tree to list of classifications for split()
            classifications = getClassificationsList()
            proc.split(classifications, strategy=SplittingStrategy.EAGER)
            
            # Check how many groups
            groups = proc.doc_groups
            print(f"📊 Found {len(groups) if groups else 1} document(s)")
            
            if groups and len(groups) > 1:
                # Multiple documents - extract each
                return self._extractMultiple(proc, extractor, vision, loaderName)
            else:
                # Single document
                return self._extractSingle(proc, extractor, filePath, vision, loaderName)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._err(str(e)[:100])
    
    def _extractSingle(self, proc: Process, extractor: Extractor, filePath: str, vision: bool, loaderName: str) -> Dict:
        """Extract single document"""
        # Classify using list of classifications
        result = extractor.classify(filePath, getClassificationsList(), vision=vision)
        
        if not result or result.name == "Other":
            return self._ok(category="Other", loader=loaderName, vision=vision)
        
        # Extract
        contract = result.classification.contract if result.classification else None
        data = None
        
        if contract:
            r = extractor.extract(filePath, contract, vision=vision, completion_strategy=self._strategy)
            data = r.model_dump() if hasattr(r, 'model_dump') else r
        
        catName = self._findCategory(result.name)
        
        return self._ok(
            category=catName or result.name,
            docType=result.name,
            data=data,
            confidence=getattr(result, 'confidence', None),
            loader=loaderName,
            vision=vision
        )
    
    def _extractMultiple(self, proc: Process, extractor: Extractor, vision: bool, loaderName: str) -> Dict:
        """Extract multiple documents - one per group"""
        print("📄 Extracting multiple documents...")
        
        documents = []
        groups = proc.doc_groups
        
        for i, group in enumerate(groups):
            print(f"  Processing group {i+1}/{len(groups)}...")
            
            # group.classification is a STRING (document type name), not object!
            docTypeName = group.classification if hasattr(group, 'classification') else None
            
            if not docTypeName:
                print(f"    ⚠️ No classification for group {i+1}")
                continue
            
            # Find category and contract from name
            catName = self._findCategory(docTypeName)
            contract = self._getContractByName(docTypeName)
            
            if not contract:
                print(f"    ⚠️ No contract for {docTypeName}")
                continue
            
            try:
                # Extract using the contract
                pages = group.pages if hasattr(group, 'pages') else []
                
                r = extractor.extract(proc.file_path, contract, vision=vision, completion_strategy=self._strategy)
                data = r.model_dump() if hasattr(r, 'model_dump') else r
                
                documents.append({
                    "category": catName,
                    "docType": docTypeName,
                    "data": data,
                    "confidence": group.confidence if hasattr(group, 'confidence') else None,
                    "_debug": {"loader": loaderName, "vision": vision, "pages": len(pages)}
                })
                print(f"    ✅ Extracted: {docTypeName}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
        
        return {"documents": documents, "error": None}
    
    def _findCategoryFromResult(self, result) -> Optional[str]:
        """Find category from extraction result"""
        # Try to find from class name
        className = result.__class__.__name__
        for node in CLASSIFICATION_TREE.nodes:
            for child in node.children:
                if child.classification.contract and child.classification.contract.__name__ == className:
                    return node.name
        return None
    
    def _findCategory(self, docTypeName: str) -> Optional[str]:
        for node in CLASSIFICATION_TREE.nodes:
            if hasattr(node, 'children'):
                for child in node.children:
                    if child.name == docTypeName:
                        return node.name
        return None
    
    def _getContractByName(self, docTypeName: str):
        """Get contract class by document type name"""
        for node in CLASSIFICATION_TREE.nodes:
            if hasattr(node, 'children'):
                for child in node.children:
                    if child.name == docTypeName:
                        return child.classification.contract
        return None
    
    def _docaiLoader(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.documentAi.credentialsPath
        return DocumentLoaderGoogleDocumentAI(GoogleDocAIConfig(
            project_id=config.documentAi.projectId,
            location=config.documentAi.location,
            processor_id=config.documentAi.processorId,
            credentials=config.documentAi.credentialsPath,
        ))
    
    def _hasText(self, path: str) -> bool:
        try:
            import fitz
            doc = fitz.open(path)
            text = "".join(doc[i].get_text() for i in range(min(3, len(doc))))
            doc.close()
            return len(text.strip()) >= 50
        except:
            return False
    
    def _ok(self, category=None, docType=None, data=None, confidence=None, loader="?", vision=False):
        return {"documents": [{
            "category": category, "docType": docType, "data": data,
            "confidence": confidence, "_debug": {"loader": loader, "vision": vision}
        }], "error": None}
    
    def _err(self, msg: str):
        return {"documents": [], "error": msg}


DocumentAIProcessor = DocumentProcessor
