import os
from dotenv import load_dotenv
from extract_thinker import (
    Extractor,
    Classification,
    DocumentLoaderGoogleDocumentAI,
    GoogleDocAIConfig,
)
from extract_thinker.models.completion_strategy import CompletionStrategy
from contracts import IDENTITY_DOCS, VEHICLE_DOCS, FINANCE_DOCS

load_dotenv()


class DocumentAIProcessor:
    
    def __init__(self):
        # Gemini API (AI Studio): gemini/model-name
        self.model = "gemini/gemini-2.0-flash"
        self.project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
        self.location = os.getenv("DOCUMENTAI_LOCATION", "us")
        self.processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
        self.credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        # Phân loại cấp 1: Nhóm văn bản
        self.category_classifications = [
            Classification(name="identity", description="Giấy tờ tùy thân: CCCD, hộ chiếu, giấy khai sinh"),
            Classification(name="vehicle", description="Giấy tờ phương tiện: bằng lái, đăng ký xe, đăng kiểm"),
            Classification(name="finance", description="Giấy tờ tài chính: hợp đồng, hóa đơn, biên lai, bill chuyển khoản"),
        ]
        
        # Phân loại cấp 2: Loại cụ thể theo từng nhóm
        self.doc_classifications = {
            "identity": self._build_classifications(IDENTITY_DOCS, "Giấy tờ tùy thân"),
            "vehicle": self._build_classifications(VEHICLE_DOCS, "Giấy tờ phương tiện"),
            "finance": self._build_classifications(FINANCE_DOCS, "Giấy tờ tài chính"),
        }
        
        print(f"✅ DocumentAI Processor (2-Level Classification)")

    def _build_classifications(self, docs: dict, desc: str) -> list:
        """Xây dựng danh sách Classification từ dict"""
        classifications = []
        for code, (name, contract) in docs.items():
            classifications.append(Classification(
                name=name,
                description=f"{desc}: {name}",
                contract=contract
            ))
        return classifications

    def _create_extractor(self) -> Extractor:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        
        config = GoogleDocAIConfig(
            project_id=self.project_id,
            location=self.location,
            processor_id=self.processor_id,
            credentials=self.credentials_path
        )
        
        extractor = Extractor()
        extractor.load_document_loader(DocumentLoaderGoogleDocumentAI(config))
        extractor.load_llm(self.model)
        return extractor

    def run(self, file_path: str) -> dict:
        try:
            extractor = self._create_extractor()
            
            # === BƯỚC 1: Phân loại NHÓM (identity / vehicle / finance) ===
            print("🔍 Bước 1: Phân loại nhóm...")
            category_result = extractor.classify(file_path, self.category_classifications)
            
            if category_result is None or not hasattr(category_result, 'name'):
                return {
                    "classification": "Chưa nhận dạng được nhóm văn bản",
                    "category": None,
                    "confidence": 0,
                    "data": None
                }
            
            category = category_result.name
            print(f"   → Nhóm: {category}")
            print(f"   → Classification Raw: {category_result}")
            
            # === BƯỚC 2: Phân loại LOẠI cụ thể trong nhóm ===
            print("🔍 Bước 2: Phân loại loại văn bản...")
            doc_classifications = self.doc_classifications.get(category, [])
            
            if not doc_classifications:
                return {
                    "classification": f"Nhóm {category} không có loại văn bản nào",
                    "category": category,
                    "confidence": 0,
                    "data": None
                }
            
            doc_result = extractor.classify(file_path, doc_classifications)
            
            if doc_result is None or not hasattr(doc_result, 'name'):
                return {
                    "classification": f"Chưa nhận dạng được loại văn bản trong nhóm {category}",
                    "category": category,
                    "confidence": 0,
                    "data": None
                }
            
            doc_type = doc_result.name
            confidence = getattr(doc_result, "confidence", 0)
            print(f"   → Loại: {doc_type} (Độ tin cậy: {confidence}/10)")
            
            # === BƯỚC 3: Trích xuất thông tin theo Contract ===
            print("📋 Bước 3: Trích xuất thông tin...")
            contract = next((c.contract for c in doc_classifications if c.name == doc_type), None)
            data = None
            
            if contract:
                try:
                    extracted = extractor.extract(
                        file_path, 
                        contract,
                        completion_strategy=CompletionStrategy.CONCATENATE
                    )
                    data = extracted.model_dump() if extracted else None
                    print(f"   → Đã trích xuất {len(data) if data else 0} trường")
                    if data:
                        print(f"   → Data Raw: {data}")
                except Exception as extract_err:
                    print(f"   ⚠️ Lỗi trích xuất: {extract_err}")
                    data = None
            
            return {
                "classification": doc_type,
                "category": category,
                "confidence": confidence,
                "data": data
            }

        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return {
                "classification": "Lỗi xử lý",
                "category": None,
                "confidence": 0,
                "data": None
            }