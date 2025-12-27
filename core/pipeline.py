import os
import nest_asyncio
from typing import Dict, Optional
import traceback

from extract_thinker import (
    Process, Extractor, ImageSplitter, TextSplitter, SplittingStrategy, CompletionStrategy, LLM
)
from core.config import config
from core.classifications import getClassificationsList
from core.utils import (
    countPages, findCategory, sanitizePageGroups, 
    makeSuccessResponse, makeErrorResponse
)

nest_asyncio.apply()

class DocumentProcessor:
    # Class xử lý tài liệu chính của hệ thống.
    def __init__(self, model: Optional[str] = None, 
                 strategy: CompletionStrategy = CompletionStrategy.CONCATENATE):
        config.validate()
        self._model = model or config.processing.model
        self._strategy = strategy
    
    def run(self, filePath: str) -> Dict:
        # Hàm chính để xử lý tài liệu và trích xuất thông tin.
        
        # Args:
        #     filePath (str): Đường dẫn tuyệt đối đến file cần xử lý.
            
        # Returns:
        #     Dict: Kết quả trích xuất hoặc thông báo lỗi.
        if not os.path.exists(filePath):
            return makeErrorResponse("File không tồn tại")
        
        try:
            # 1. Khởi tạo Loader và đếm số trang
            loader, vision, loaderName = config.createLoader(filePath)
            pageCount = countPages(filePath)
            
            print(f"🔄 Đang xử lý: {loaderName}, vision={vision}, số trang={pageCount}")
            
            # 2. Cấu hình Extractor
            extractor = Extractor()
            extractor.load_document_loader(loader)
            extractor.load_llm(LLM(self._model))
            
            # 3. Chọn chiến lược xử lý dựa trên số trang
            if pageCount == 1:
                return self.extractSinglePage(extractor, filePath, vision, loaderName)
            
            return self.extractMultiPage(filePath, vision, loaderName, pageCount)
                
        except Exception as e:
            traceback.print_exc()
            return makeErrorResponse(str(e)[:200])
    
    def extractSinglePage(self, extractor: Extractor, filePath: str, vision: bool, loaderName: str) -> Dict:
        # Xử lý tài liệu đơn trang (Single Page).
        # Phân loại tài liệu
        classifications = getClassificationsList()
        result = extractor.classify(filePath, classifications, vision=vision)
        
        if not result or result.name == "Other":
            return makeSuccessResponse(category="Other", loader=loaderName, vision=vision)
        
        contract = result.classification.contract if result.classification else None
        data = None
        
        # Trích xuất dữ liệu nếu tìm thấy Contract phù hợp
        if contract:
            extractedObj = extractor.extract(filePath, contract, vision=vision, completion_strategy=self._strategy)
            data = extractedObj.model_dump() if hasattr(extractedObj, 'model_dump') else extractedObj
        
        return makeSuccessResponse(
            category=findCategory(result.name) or result.name,
            docType=result.name,
            data=data,
            confidence=getattr(result, 'confidence', None),
            loader=loaderName,
            vision=vision
        )
    
    def extractMultiPage(self, filePath: str, vision: bool, loaderName: str, pageCount: int) -> Dict:
        # Xử lý tài liệu đa trang (Multi Page).
        # Bao gồm các bước: Split (Tách trang) -> Sanitize (Sửa lỗi trang) -> Extract (Trích xuất).
        print("📄 Phát hiện tài liệu nhiều trang. Đang tiến hành tách (Splitting)...")
        
        # 1. Chuẩn bị Loader riêng biệt cho bước Split
        splitLoader, _, _ = config.createLoader(filePath)
        
        extractor = Extractor()
        extractor.load_llm(LLM(self._model))
        
        # Dummy loader cho extractor (cần thiết cho init)
        dummyLoader, _, _ = config.createLoader(filePath)
        extractor.load_document_loader(dummyLoader)
        
        proc = Process()
        proc.load_document_loader(splitLoader)
        proc.add_classify_extractor([[extractor]])
        
        # Chọn Splitter phù hợp (Image hoặc Text)
        splitter = ImageSplitter(self._model) if vision else TextSplitter(self._model)
        proc.load_splitter(splitter)
        proc.load_file(filePath)
        
        classifications = getClassificationsList()
        for c in classifications:
            c.extractor = extractor
        
        # 2. Thực hiện tách trang (Split)
        # Sử dụng EAGER mode nếu ít trang, LAZY mode nếu nhiều trang để tối ưu
        strategy = SplittingStrategy.EAGER if pageCount <= config.processing.eagerPageThreshold else SplittingStrategy.LAZY
        
        try:
            proc.split(classifications, strategy=strategy)
        except KeyError as e:
            # Fallback: Nếu ImageSplitter lỗi (thường do file không có ảnh), thử lại bằng TextSplitter
            if 'image' in str(e) and vision:
                print("⚠️ Fallback sang TextSplitter do lỗi xử lý ảnh.")
                proc.load_splitter(TextSplitter(self._model))
                proc.split(classifications, strategy=strategy)
            else:
                raise e
        
        groups = proc.doc_groups or []
        print(f"📊 Tìm thấy {len(groups)} nhóm tài liệu.")
        
        # 3. Sửa lỗi phân trang (Validation & Correction)
        sanitizePageGroups(groups, pageCount)

        # 4. Trích xuất thông tin (Extract)
        print("📝 Đang trích xuất (Process.extract)...")
        
        try:
            results = proc.extract(vision=vision, completion_strategy=self._strategy)
            
            documents = []
            for group, data in zip(groups, results):
                dataDict = data.model_dump() if hasattr(data, 'model_dump') else data
                documents.append({
                    "category": findCategory(group.classification),
                    "docType": group.classification,
                    "data": dataDict,
                    "confidence": getattr(group, 'confidence', None),
                    "_debug": {"loader": loaderName, "vision": vision, "pages": len(group.pages)}
                })
                print(f"   ✅ Đã trích xuất: {group.classification}")
                
            return {"documents": documents, "error": None}
            
        except Exception as e:
            print(f"❌ Lỗi Process.extract: {e}")
            traceback.print_exc()
            return {"documents": [], "error": f"Lỗi xử lý: {str(e)}"}

# Alias để tương thích ngược nếu cần
DocumentAIProcessor = DocumentProcessor
