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
    
    def isImageFile(self, filePath: str) -> bool:
        """Check if file is an image based on extension"""
        ext = os.path.splitext(filePath)[1].lower()
        return ext in self.extensions


@dataclass
class DocumentAiConfig:
    projectId: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_PROJECT_ID", ""))
    location: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_LOCATION", "us"))
    processorId: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_PROCESSOR_ID", ""))
    credentialsPath: str = field(default_factory=lambda: os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json"))
    
    def validate(self) -> List[str]:
        """Returns list of missing required fields"""
        missing = []
        if not self.projectId:
            missing.append("DOCUMENTAI_PROJECT_ID")
        if not self.processorId:
            missing.append("DOCUMENTAI_PROCESSOR_ID")
        return missing
    
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


@dataclass
class ProcessingConfig:
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash"))
    eagerPageThreshold: int = 10
    dpi: int = 300
    enableThinking: bool = False


@dataclass
class AppConfig:
    ocr: OcrConfig = field(default_factory=OcrConfig)
    documentAi: DocumentAiConfig = field(default_factory=DocumentAiConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    
    def validate(self) -> None:
        missing = self.documentAi.validate()
        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}. "
                "Please check your .env file"
            )
    
    def createLoader(self, filePath: str):
        """
        Create appropriate loader based on file type.
        Returns: (loader, vision, loaderName)
        """
        from extract_thinker import DocumentLoaderPyPdf, DocumentLoaderSpreadSheet
        
        ext = os.path.splitext(filePath)[1].lower()
        
        # Image or scanned PDF -> DocAI
        if self.ocr.isImageFile(filePath) or (ext == '.pdf' and not self._pdfHasText(filePath)):
            return self.documentAi.createLoader(), True, "docai"
        
        # Excel files
        if ext in EXCEL_EXT:
            return DocumentLoaderSpreadSheet(), False, "spreadsheet"
        
        # Default: PyPdf for text-based PDFs
        return DocumentLoaderPyPdf(), False, "pypdf"
    
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
