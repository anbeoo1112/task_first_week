"""
Configuration - Centralized settings management
Clean, type-safe configuration with dataclasses
"""
import os
from dataclasses import dataclass, field
from typing import Set, List
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class OcrConfig:
    """OCR-related configuration"""
    extensions: Set[str] = field(default_factory=lambda: {
        '.png', '.jpg', '.jpeg', '.tiff', '.gif', '.bmp', '.webp'
    })
    
    def isImageFile(self, filePath: str) -> bool:
        """Check if file is an image based on extension"""
        ext = os.path.splitext(filePath)[1].lower()
        return ext in self.extensions


@dataclass
class DocumentAiConfig:
    """Google Document AI configuration"""
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


@dataclass
class ProcessingConfig:
    """Processing settings"""
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash"))
    maxPdfPages: int = field(default_factory=lambda: int(os.getenv("MAX_PDF_PAGES", "10")))
    dpi: int = 300
    enableThinking: bool = False


@dataclass
class AppConfig:
    """Main application configuration"""
    ocr: OcrConfig = field(default_factory=OcrConfig)
    documentAi: DocumentAiConfig = field(default_factory=DocumentAiConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    
    def validate(self) -> None:
        """Validate all required configurations"""
        missing = self.documentAi.validate()
        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}. "
                "Please check your .env file"
            )


# Singleton instance
config = AppConfig()
