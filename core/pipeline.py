import os
import tempfile
from dotenv import load_dotenv
from extract_thinker import (
    Extractor,
    Classification,
    DocumentLoaderGoogleDocumentAI,
    GoogleDocAIConfig,
    DocumentLoaderMarkItDown,
    DocumentLoaderPyPdf,
)
from contracts import IDENTITY_DOCS, VEHICLE_DOCS, FINANCE_DOCS

# Optional imports
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

load_dotenv()

# Extensions
OCR_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.gif', '.bmp', '.webp'}
OFFICE_EXTENSIONS = {'.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.txt', '.html', '.xml', '.json', '.csv'}


class DocumentAIProcessor:
    
    def __init__(self):
        self.model = "gemini/gemini-2.0-flash"
        self.project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
        self.location = os.getenv("DOCUMENTAI_LOCATION", "us")
        self.processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
        self.credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        self.category_classifications = [
            Classification(name="identity", description="Giấy tờ tùy thân: CCCD, hộ chiếu, giấy khai sinh"),
            Classification(name="vehicle", description="Giấy tờ phương tiện: bằng lái, đăng ký xe, đăng kiểm"),
            Classification(name="finance", description="Giấy tờ tài chính: hợp đồng, hóa đơn, biên lai, bill chuyển khoản"),
            Classification(name="Other", description="Các loại giấy tờ khác", contract=None)
        ]
        
        self.doc_classifications = {
            "identity": self._build_classifications(IDENTITY_DOCS, "Giấy tờ tùy thân"),
            "vehicle": self._build_classifications(VEHICLE_DOCS, "Giấy tờ phương tiện"),
            "finance": self._build_classifications(FINANCE_DOCS, "Giấy tờ tài chính"),
            "Other": []
        }
        print("DocumentAI Processor (Smart PDF)")

    def _build_classifications(self, docs: dict, desc: str) -> list:
        return [Classification(name=name, description=f"{desc}: {name}", contract=contract) 
                for code, (name, contract) in docs.items()]

    def _get_documentai_loader(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        config = GoogleDocAIConfig(
            project_id=self.project_id, location=self.location,
            processor_id=self.processor_id, credentials=self.credentials_path,
            enable_native_pdf_parsing=True
        )
        return DocumentLoaderGoogleDocumentAI(config)

    def _pdf_has_text(self, file_path: str) -> bool:
        """Check if PDF has text layer (from Word) or is scanned."""
        if not PYPDF_AVAILABLE:
            return False
        try:
            reader = PdfReader(file_path)
            text = reader.pages[0].extract_text() if reader.pages else ""
            return len((text or "").strip()) > 50
        except:
            return False

    def run(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {"classification": "Lỗi", "message": "File không tồn tại", "data": None}

        try:
            ext = os.path.splitext(file_path)[1].lower()
            
            # PDF: Smart detection
            if ext == '.pdf':
                if self._pdf_has_text(file_path):
                    print("PDF text-based (từ Word) - PyPDF")
                    return self._classify_and_extract(file_path, DocumentLoaderPyPdf())
                else:
                    print("PDF scanned - convert to image")
                    return self._process_scanned_pdf(file_path)
            
            # Images: Document AI OCR
            elif ext in OCR_EXTENSIONS:
                print(f"Image - Document AI OCR")
                return self._classify_and_extract(file_path, self._get_documentai_loader(), vision=True)
            
            # Office: MarkItDown
            elif ext in OFFICE_EXTENSIONS:
                print(f"Office file - MarkItDown")
                return self._classify_and_extract(file_path, DocumentLoaderMarkItDown())
            
            else:
                return {"classification": "Lỗi", "message": f"Không hỗ trợ {ext}", "data": None}

        except Exception as e:
            print(f"Lỗi: {e}")
            return {"classification": "Lỗi xử lý", "message": str(e), "data": None}

    def _process_scanned_pdf(self, file_path: str) -> dict:
        """Convert scanned PDF to image and process."""
        if not PDF2IMAGE_AVAILABLE:
            return self._classify_and_extract(file_path, self._get_documentai_loader())
        
        try:
            images = convert_from_path(file_path, first_page=1, last_page=1, dpi=200)
            if not images:
                return {"classification": "Lỗi", "message": "Không convert được PDF", "data": None}
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                images[0].save(tmp.name, 'PNG')
                result = self._classify_and_extract(tmp.name, self._get_documentai_loader(), vision=True)
                os.remove(tmp.name)
                return result
        except Exception as e:
            print(f"Lỗi convert: {e}")
            return {"classification": "Lỗi", "message": str(e), "data": None}

    def _classify_and_extract(self, file_path: str, loader, vision: bool = False) -> dict:
        """Core: Classify + Extract với loader bất kỳ."""
        extractor = Extractor()
        extractor.load_document_loader(loader)
        extractor.load_llm(self.model)
        
        # Bước 1: Phân loại nhóm
        print("Bước 1: Phân loại nhóm...")
        cat_result = extractor.classify(file_path, self.category_classifications)
        if not cat_result:
            return {"classification": "Không xác định", "category": None, "confidence": 0, "data": None}
        
        category = cat_result.name
        print(f"   → Nhóm: {category}")
        
        # Bước 2: Phân loại loại cụ thể
        print("Bước 2: Phân loại chi tiết...")
        sub_cls = self.doc_classifications.get(category, [])
        if not sub_cls:
            return {"classification": category, "category": category, "confidence": 10, "data": None}
        
        doc_result = extractor.classify(file_path, sub_cls)
        if not doc_result:
            return {"classification": "Không xác định", "category": category, "confidence": 0, "data": None}
        
        doc_type = doc_result.name
        confidence = getattr(doc_result, "confidence", 0)
        print(f"   → Loại: {doc_type} ({confidence}/10)")
        
        # Bước 3: Trích xuất
        contract = next((c.contract for c in sub_cls if c.name == doc_type), None)
        data = None
        if contract:
            print("ước 3: Trích xuất...")
            try:
                result = extractor.extract(file_path, contract, vision=vision) if vision else extractor.extract(file_path, contract)
                data = result.model_dump() if result else None
                print(f"{len(data) if data else 0} trường")
            except Exception as e:
                print(f"Lỗi: {e}")
        
        return {"classification": doc_type, "category": category, "confidence": confidence, "data": data}