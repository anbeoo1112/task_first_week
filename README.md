# VN Document - Vietnamese Document Processing

> Intelligent document processing for Vietnamese identity, vehicle, and financial documents.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud credentials

# Run the app
streamlit run app_cloud.py
```

If you prefer the legacy file name, you can also use:

```bash
pip install -r requirement.txt
```

## 📁 Project Structure

```
task_first_week/
├── core/
│   ├── __init__.py      # Package exports
│   ├── config.py        # Centralized configuration
│   ├── loaders.py       # Document loader factory
│   ├── classifications.py # Document type definitions
│   └── pipeline.py      # Main processing engine
├── contracts/
│   ├── identity.py      # CCCD, Passport, Birth cert
│   ├── vehicle.py       # Driver license, Vehicle reg
│   └── finance.py       # Contracts, Bank transfers
├── app_cloud.py         # Streamlit web interface
└── .env                 # Environment configuration
```

## ⚙️ Configuration

Required environment variables in `.env`:

```bash
DOCUMENTAI_PROJECT_ID=your-project-id
DOCUMENTAI_PROCESSOR_ID=your-processor-id
DOCUMENTAI_GOOGLE_CREDENTIALS=credentials.json
GEMINI_API_KEY=your-gemini-key

# Optional
MAX_PDF_PAGES=3
```

## 📄 Supported Documents

| Category | Documents |
|----------|-----------|
| 🪪 Identity | CCCD, Passport, Birth Certificate |
| 🚗 Vehicle | Driver License, Vehicle Registration, Inspection |
| 💰 Finance | Contracts, Bank Transfers |

## 🔧 Usage

### Single Document

```python
from core import DocumentProcessor

processor = DocumentProcessor()
result = processor.run("path/to/document.pdf")

print(result)
# {
#     "category": "identity",
#     "doc_type": "Căn cước công dân",
#     "data": { ... },
#     "error": None
# }
```

### Multi-Document PDF

```python
result = processor.run_multi("path/to/mixed_documents.pdf")

print(result)
# {
#     "documents": [
#         {"index": 0, "doc_type": "VietnamCCCD", "data": {...}},
#         {"index": 1, "doc_type": "VietnamVehicleReg", "data": {...}},
#     ],
#     "error": None
# }
```

## 🛠️ Technologies

- **OCR**: Google Document AI
- **LLM**: Gemini 2.0 Flash
- **Framework**: ExtractThinker
- **UI**: Streamlit

## 📝 License

MIT
