import os
from dotenv import load_dotenv
from extract_thinker import (
    Extractor,
    Classification,
    DocumentLoaderGoogleDocumentAI,
    GoogleDocAIConfig,
    DocumentLoaderMarkItDown,
    DocumentLoaderPyPdf,
    Process,
    SplittingStrategy
)
from contracts import IDENTITY_DOCS, VEHICLE_DOCS, FINANCE_DOCS

load_dotenv()

OCR_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.gif', '.bmp', '.webp'}

class DocumentAIProcessor:
    
    def __init__(self):
        self.model = "gemini/gemini-2.0-flash"
        
        self.project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
        self.location = os.getenv("DOCUMENTAI_LOCATION", "us")
        self.processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
        self.credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        # Load classifications
        self.category_classifications = [
            Classification(name="identity", description="Giấy tờ tùy thân: CCCD, hộ chiếu, giấy khai sinh"),
            Classification(name="vehicle", description="Giấy tờ phương tiện: bằng lái, đăng ký xe, đăng kiểm"),
            Classification(name="finance", description="Giấy tờ tài chính: hợp đồng, hóa đơn, biên lai, bill chuyển khoản"),
            Classification(name="Other", description="Các loại giấy tờ khác", contract=None)
        ]

        self.doc_classifications = {
            "identity": self.buildClassifications(IDENTITY_DOCS, "Giấy tờ tùy thân"),
            "vehicle": self.buildClassifications(VEHICLE_DOCS, "Giấy tờ phương tiện"),
            "finance": self.buildClassifications(FINANCE_DOCS, "Giấy tờ tài chính"),
            "Other": []
        }

    def buildClassifications(self, docs: dict, desc: str) -> list:
        return [Classification(name=name, description=f"{desc}: {name}", contract=contract) 
                for code, (name, contract) in docs.items()]

    def getDocumentAiLoader(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        config = GoogleDocAIConfig(
            project_id=self.project_id, location=self.location,
            processor_id=self.processor_id, credentials=self.credentials_path,
            enable_native_pdf_parsing=True
        )
        return DocumentLoaderGoogleDocumentAI(config)
    
    def pdfHasText(self, file_path: str) -> bool:
        try:
            loader = DocumentLoaderPyPdf()
            document = loader.load(file_path)
            if isinstance(document, list):
                for page in document:
                    content = getattr(page, 'content', '') or getattr(page, 'text', '') or str(page)
                    if content.strip(): return True
            elif hasattr(document, 'pages'):
                for page in document.pages:
                    if page.text.strip(): return True
            elif hasattr(document, 'content'):
                return bool(document.content.strip())
            return False
        except Exception:
            return False
    
    def getLoaderForFile(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in OCR_EXTENSIONS:
            return self.getDocumentAiLoader()
        elif ext == '.pdf':
            if self.pdfHasText(file_path):
                return DocumentLoaderPyPdf()
            else:
                return self.getDocumentAiLoader()
        else:
            return DocumentLoaderMarkItDown()

    def run(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext in OCR_EXTENSIONS:
                return self.runWithExtractor(file_path)
            else:
                return self.runWithProcess(file_path)
        except Exception as e:
            return {"error": str(e), "category": None, "doc_type": None, "data": None}
    
    def runWithExtractor(self, file_path: str) -> dict:
        loader = self.getDocumentAiLoader()
        extractor = Extractor()
        extractor.load_document_loader(loader)
        extractor.load_llm(self.model)
        
        # 1. Phân loại Category
        category_result = extractor.classify(file_path, self.category_classifications)
        if not category_result:
            return {"error": "Không nhận dạng được Category", "category": None, "doc_type": None, "data": None}
        
        category_name = category_result.name
        if category_name == "Other":
            return {"category": category_name, "doc_type": None, "data": None}
        
        # 2. Phân loại Doc Type
        doc_classifications = self.doc_classifications.get(category_name, [])
        if not doc_classifications:
            return {"category": category_name, "doc_type": None, "data": None}
        
        doc_result = extractor.classify(file_path, doc_classifications)
        if not doc_result:
            return {"category": category_name, "doc_type": None, "data": None}
        
        # 3. Trích xuất (Fix: Lấy contract trực tiếp từ doc_result)
        extracted_data = None
        if doc_result.contract:
            extracted_data = extractor.extract(file_path, doc_result.contract)
        
        return {
            "category": category_name,
            "doc_type": doc_result.name,
            "data": extracted_data
        }
    
    def runWithProcess(self, file_path: str) -> dict:
        try:
            loader = self.getLoaderForFile(file_path)
            
            # --- SETUP PROCESS ---
            process = Process()
            process.load_document_loader(loader)
            
            # FIX 1: Load Classifier phải truyền MODEL string, không phải list classification
            process.load_classifier(self.model) 
            
            # SplittingStrategy giúp đọc file PDF ngay lập tức
            process.load_splitting_strategy(SplittingStrategy.EAGER)
            
            # --- 1. Phân loại Category ---
            result = process.classify(file_path, self.category_classifications)
            if not result:
                return {"error": "Không nhận dạng được Category", "category": None, "doc_type": None, "data": None}
            
            category_name = result.name
            if category_name == "Other":
                return {"category": category_name, "doc_type": None, "data": None}
            
            # --- 2. Phân loại Doc Type ---
            doc_classifications = self.doc_classifications.get(category_name, [])
            if not doc_classifications:
                return {"category": category_name, "doc_type": None, "data": None}
            
            doc_result = process.classify(file_path, doc_classifications)
            if not doc_result:
                return {"category": category_name, "doc_type": None, "data": None}
            
            # --- 3. Trích xuất ---
            extracted_data = None
            
            target_contract = doc_result.contract 

            if target_contract:
                extractor = Extractor()
                extractor.load_document_loader(loader)
                extractor.load_llm(self.model)
                extracted_data = extractor.extract(file_path, target_contract)
            
            return {
                "category": category_name,
                "doc_type": doc_result.name,
                "data": extracted_data
            }

        except Exception as e:
            return {"error": str(e), "category": None, "doc_type": None, "data": None}