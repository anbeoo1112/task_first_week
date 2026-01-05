# VN Document - Xử Lý Tài Liệu Tiếng Việt

> Xử lý tài liệu thông minh cho các loại giấy tờ tùy thân, phương tiện và tài chính của Việt Nam.

## 🚀 Bắt đầu nhanh

```bash
# Cài đặt thư viện dependencies
pip install -r requirements.txt

# Cấu hình môi trường
cp .env.example .env
# Chỉnh sửa file .env với thông tin Google Cloud credentials của bạn

# Chạy ứng dụng
streamlit run app_cloud.py
```

Nếu bạn muốn dùng tên file cũ, bạn có thể chạy lệnh:

```bash
pip install -r requirement.txt
```

## 📁 Cấu trúc dự án

```
task_first_week/
├── core/
│   ├── __init__.py      # Package exports
│   ├── config.py        # Cấu hình tập trung
│   ├── loaders.py       # Document loader factory
│   ├── classifications.py # Định nghĩa các loại tài liệu
│   └── pipeline.py      # Engine xử lý chính
├── contracts/
│   ├── identity.py      # CCCD, Hộ chiếu, Giấy khai sinh
│   ├── vehicle.py       # Bằng lái, Đăng ký xe, Đăng kiểm
│   └── finance.py       # Hợp đồng, Chuyển khoản
├── app_cloud.py         # Giao diện web Streamlit
└── .env                 # Cấu hình môi trường
```

## ⚙️ Cấu hình

Các biến môi trường bắt buộc trong `.env`:

```bash
DOCUMENTAI_PROJECT_ID=your-project-id
DOCUMENTAI_PROCESSOR_ID=your-processor-id
DOCUMENTAI_GOOGLE_CREDENTIALS=credentials.json
GEMINI_API_KEY=your-gemini-key

# Tùy chọn
MAX_PDF_PAGES=3
```

## 📄 Các loại tài liệu hỗ trợ

| Danh mục | Tài liệu |
|----------|-----------|
| 🪪 Giấy tờ tùy thân | CCCD, Hộ chiếu, Giấy khai sinh |
| 🚗 Phương tiện | Giấy phép lái xe, Đăng ký xe, Đăng kiểm |
| 💰 Tài chính | Hợp đồng, Ủy nhiệm chi / Chuyển khoản |

## 🔧 Cách sử dụng

### Xử lý một tài liệu

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

### Xử lý PDF nhiều loại giấy tờ (Multi-Document)

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

## 🛠️ Công nghệ sử dụng

- **OCR**: Google Document AI
- **LLM**: Gemini 2.0 Flash
- **Framework**: ExtractThinker
- **UI**: Streamlit

## 📝 License

MIT
