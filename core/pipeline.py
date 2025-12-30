import os
import nest_asyncio
from typing import Dict, Optional, Any

from extract_thinker import (
    Extractor, CompletionStrategy, LLM
)
from extract_thinker.document_loader.document_loader_data import DocumentLoaderData

from core.config import config
from core.classifications import getClassificationsList, CLASSIFICATION_TREE

def findCategory(docTypeName: str) -> Optional[str]:
    """Tìm category (nhóm) dựa trên doc_type_name."""
    for node in CLASSIFICATION_TREE.nodes:
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                if child.name == docTypeName:
                    return node.name
    return None

def makeSuccessResponse(
    category: Optional[str] = None, 
    docType: Optional[str] = None, 
    data: Any = None, 
    confidence: Optional[float] = None, 
    loader: str = "?", 
    vision: bool = False
) -> Dict:
    """Tạo response thành công chuẩn hóa."""
    return {"documents": [{
        "category": category, 
        "docType": docType, 
        "data": data,
        "confidence": confidence,
        "_debug": {"loader": loader, "vision": vision}
    }], "error": None}

def makeErrorResponse(msg: str) -> Dict:
    """Tạo response lỗi chuẩn hóa."""
    return {"documents": [], "error": msg}


nest_asyncio.apply()


class DocumentProcessor:
    """
    Bộ xử lý tài liệu - Wrapper cho extract_thinker.
    """
    
    def __init__(self, model: Optional[str] = None, 
                 strategy: CompletionStrategy = CompletionStrategy.CONCATENATE):
        config.validate()
        self._model = model or config.processing.model
        self._strategy = strategy
        # Tạo LLM một lần duy nhất, dùng lại cho mọi request
        self._llm = LLM(self._model)
    
    
    def run(self, filePath: str) -> Dict:
        """Entry point chính - xử lý file trực tiếp, tắt vision."""
        if not os.path.exists(filePath):
            return makeErrorResponse("File không tồn tại")
        
        try:
            # 1. Load document (1 lần duy nhất)
            loader, _, loaderName = config.createLoader(filePath)
            pages = loader.load(filePath)
            
            print(f"🔄 Xử lý: {loaderName}, {len(pages) if isinstance(pages, list) else 1} trang (Pre-loaded)")
            
            # 2. Xử lý với content đã load
            return self._process(pages, filePath, loaderName)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return makeErrorResponse(str(e)[:200])
    
    def _process(self, pages, filePath: str, loaderName: str) -> Dict:
        """
        Xử lý tài liệu với Extractor:
        - Sử dụng DocumentLoaderData để xử lý content đã load (tránh đọc file 2 lần).
        - Extractor tự động xử lý merge/paginate cho tài liệu nhiều trang.
        """
        # Setup Extractor với DocumentLoaderData (để nhận raw data)
        extractor = Extractor()
        extractor.load_document_loader(DocumentLoaderData())
        extractor.load_llm(self._llm)
        
        # Phân loại (đưa pages vào trực tiếp)
        classifications = getClassificationsList()
        result = extractor.classify(pages, classifications, vision=False)
        confidence = getattr(result, 'confidence', None)
        
        if not result or result.name == "Other":
            return makeSuccessResponse(category="Other", loader=loaderName, vision=False)
        
        # Trích xuất
        contract = result.classification.contract if result.classification else None
        data = None
        
        if contract:
            print(f"📄 Loại: {result.name}. Trích xuất...")
            
            # Lấy extra_content
            from contracts import EXTRA_CONTENTS
            extra = EXTRA_CONTENTS.get(contract, None)
            
            # Extract (đưa pages vào trực tiếp, Extractor tự handle strategy)
            extracted = extractor.extract(
                pages, contract, 
                vision=False,
                content=extra, 
                completion_strategy=self._strategy
            )
            data = extracted.model_dump() if hasattr(extracted, 'model_dump') else extracted
        
        return makeSuccessResponse(
            category=findCategory(result.name) or result.name,
            docType=result.name,
            data=data,
            confidence=confidence,
            loader=loaderName,
            vision=False
        )


# Alias cho backward compatibility
DocumentAIProcessor = DocumentProcessor
