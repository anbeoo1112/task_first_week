"""Script kiểm tra OCR với Google Document AI"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Kiểm tra kết nối Google Document AI"""
    print("=" * 60)
    print("🔧 KIỂM TRA CẤU HÌNH")
    print("=" * 60)
    
    project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
    location = os.getenv("DOCUMENTAI_LOCATION", "us")
    processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
    credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
    
    print(f"📌 Project ID: {project_id}")
    print(f"📌 Location: {location}")
    print(f"📌 Processor ID: {processor_id}")
    print(f"📌 Credentials: {credentials_path}")
    
    # Kiểm tra file credentials tồn tại
    if os.path.exists(credentials_path):
        print(f"✅ File credentials tồn tại")
        import json
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
            print(f"   → Service Account: {creds.get('client_email', 'N/A')}")
    else:
        print(f"❌ File credentials KHÔNG tồn tại: {credentials_path}")
        return False
    
    return True


def test_ocr_with_extract_thinker(file_path: str):
    """Test OCR qua extract_thinker"""
    print("\n" + "=" * 60)
    print("🔍 TEST OCR VỚI EXTRACT_THINKER")
    print("=" * 60)
    
    try:
        from extract_thinker import DocumentLoaderGoogleDocumentAI, GoogleDocAIConfig
        
        config = GoogleDocAIConfig(
            project_id=os.getenv("DOCUMENTAI_PROJECT_ID"),
            location=os.getenv("DOCUMENTAI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENTAI_PROCESSOR_ID"),
            credentials=os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        )
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        loader = DocumentLoaderGoogleDocumentAI(config)
        print(f"📁 Loading file: {file_path}")
        
        result = loader.load(file_path)
        
        print(f"\n✅ OCR thành công!")
        print(f"📄 Số pages: {len(result) if isinstance(result, list) else 1}")
        print("\n" + "-" * 40)
        print("📝 NỘI DUNG OCR:")
        print("-" * 40)
        
        if isinstance(result, list):
            for i, page in enumerate(result):
                print(f"\n--- Page {i+1} ---")
                if isinstance(page, dict):
                    print(page.get("content", page))
                else:
                    print(page)
        else:
            print(result)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Lỗi: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_ocr_direct_api(file_path: str):
    """Test OCR trực tiếp với Google Document AI API"""
    print("\n" + "=" * 60)
    print("🔍 TEST OCR TRỰC TIẾP VỚI GOOGLE API")
    print("=" * 60)
    
    try:
        from google.cloud import documentai_v1 as documentai
        from google.api_core.client_options import ClientOptions
        
        project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
        location = os.getenv("DOCUMENTAI_LOCATION", "us")
        processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
        credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        # Đọc file
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        # Xác định mime type
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".tiff": "image/tiff",
            ".tif": "image/tiff",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
        }
        mime_type = mime_types.get(ext, "application/octet-stream")
        print(f"📁 File: {file_path}")
        print(f"📌 MIME Type: {mime_type}")
        print(f"📌 File size: {len(file_content) / 1024:.2f} KB")
        
        # Tạo client
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        
        # Tạo request
        name = client.processor_path(project_id, location, processor_id)
        print(f"📌 Processor path: {name}")
        
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        
        print("\n⏳ Đang gọi API...")
        result = client.process_document(request=request)
        document = result.document
        
        print(f"\n✅ OCR thành công!")
        print(f"📄 Số pages: {len(document.pages)}")
        print("\n" + "-" * 40)
        print("📝 NỘI DUNG OCR:")
        print("-" * 40)
        print(document.text[:2000] if len(document.text) > 2000 else document.text)
        
        if len(document.text) > 2000:
            print(f"\n... (còn {len(document.text) - 2000} ký tự)")
        
        return document.text
        
    except Exception as e:
        print(f"\n❌ Lỗi: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys
    
    print("🚀 KIỂM TRA GOOGLE DOCUMENT AI OCR")
    print("=" * 60)
    
    if not test_connection():
        print("\n❌ Kiểm tra cấu hình thất bại!")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("\n⚠️  Chưa có file để test OCR")
        print("Usage: python test_ocr.py <file_path> [extract_thinker|direct]")
        print("\nVí dụ:")
        print("  python test_ocr.py document.pdf")
        print("  python test_ocr.py image.png direct")
        sys.exit(0)
    
    file_path = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "extract_thinker"
    
    if not os.path.exists(file_path):
        print(f"\n❌ File không tồn tại: {file_path}")
        sys.exit(1)
    
    if method == "direct":
        test_ocr_direct_api(file_path)
    else:
        test_ocr_with_extract_thinker(file_path)
