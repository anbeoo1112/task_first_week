import os
from dataclasses import dataclass, field
from typing import Set, List
from dotenv import load_dotenv

load_dotenv()

EXCEL_EXT = {'.xlsx', '.xls', '.xlsm', '.xlsb', '.ods'}


@dataclass(frozen=True)
class OcrConfig:
    extensions: Set[str] = field(default_factory=lambda: {
        '.png', '.jpg', '.jpeg', '.tiff', '.gif', '.bmp', '.webp'
    })
    
    # Kiểm tra file có phải là file ảnh không
    def isImageFile(self, filePath: str) -> bool:
        """Check if file is an image based on extension"""
        ext = os.path.splitext(filePath)[1].lower()
        return ext in self.extensions

#Lớp config cho DocumentAI
@dataclass
class DocumentAiConfig:
    projectId: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_PROJECT_ID", ""))
    location: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_LOCATION", "us"))
    processorId: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_PROCESSOR_ID", ""))
    credentialsPath: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json"))
    
    # Kiểm tra các tham số cần thiết
    def validate(self) -> List[str]:
        """Returns list of missing required fields"""
        missing = []
        if not self.projectId:
            missing.append("DOCUMENTAI_PROJECT_ID")
        if not self.processorId:
            missing.append("DOCUMENTAI_PROCESSOR_ID")
        return missing
    
    # Tạo loader cho DocumentAI
    def createLoader(self):
        """Create a new DocumentLoaderGoogleDocumentAI instance"""
        from extract_thinker import DocumentLoaderGoogleDocumentAI, GoogleDocAIConfig
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentialsPath
        return DocumentLoaderGoogleDocumentAI(GoogleDocAIConfig(
            project_id=self.projectId,
            location=self.location,
            processor_id=self.processorId,
            credentials=self.credentialsPath,
        ))

#Config cho Processing
@dataclass
class ProcessingConfig:
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash"))
    eagerPageThreshold: int = 10
    dpi: int = 300
    enableThinking: bool = False


#Config cho toàn bộ ứng dụng
@dataclass
class AppConfig:
    ocr: OcrConfig = field(default_factory=OcrConfig)
    documentAi: DocumentAiConfig = field(default_factory=DocumentAiConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    
    # Kiểm tra các tham số cần thiết
    def validate(self) -> None:
        missing = self.documentAi.validate()
        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}. "
                "Please check your .env file"
            )
    
    # Tạo loader phù hợp với loại file
    def createLoader(self, filePath: str):
        """
        Create appropriate loader based on file type.
        Returns: (loader, vision, loaderName)
        """
        from extract_thinker import DocumentLoaderPyPdf, DocumentLoaderSpreadSheet
        
        ext = os.path.splitext(filePath)[1].lower()
        
        # 1. Image files -> Use Document AI (OCR)
        if self.ocr.isImageFile(filePath):
            # Document AI handles OCR, no need for LLM vision
            return self.documentAi.createLoader(), False, "docai"
        
        # 2. Excel files
        if ext in EXCEL_EXT:
            return DocumentLoaderSpreadSheet(), False, "spreadsheet"
        
        # 3. PDF files
        if ext == '.pdf':
            if self._pdfHasText(filePath):
                # Native Text PDF -> No Vision
                return DocumentLoaderPyPdf(), False, "pypdf"
            else:
                # Scanned PDF -> Enable VisionFor LLM (Gemini)
                return DocumentLoaderPyPdf(), True, "pypdf_vision"
        
        # Default fallback
        return DocumentLoaderPyPdf(), False, "pypdf"
    
    # Kiểm tra PDF có selectable text không
    def _pdfHasText(self, path: str) -> bool:
        """Check if PDF has selectable text"""
        try:
            import fitz
            doc = fitz.open(path)
            text = "".join(doc[i].get_text() for i in range(min(3, len(doc))))
            doc.close()
            return len(text.strip()) >= 50
        except:
            return False


# Singleton instance
config = AppConfig()
