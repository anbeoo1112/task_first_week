"""Test suy luận với extract_thinker + Ollama"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_ollama_direct():
    """Test Ollama trực tiếp"""
    print("=" * 60)
    print("🧠 TEST OLLAMA TRỰC TIẾP")
    print("=" * 60)
    
    import requests
    
    prompt = "Xin chào, bạn là ai?"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama hoạt động!")
            print(f"📝 Response: {result.get('response', 'N/A')[:500]}")
            return True
        else:
            print(f"❌ Lỗi: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Lỗi kết nối Ollama: {e}")
        return False


def test_litellm():
    """Test LiteLLM với Ollama"""
    print("\n" + "=" * 60)
    print("🧠 TEST LITELLM + OLLAMA")
    print("=" * 60)
    
    try:
        from litellm import completion
        
        response = completion(
            model="ollama/qwen2.5:3b",
            messages=[{"role": "user", "content": "Xin chào, bạn là ai?"}],
            api_base="http://localhost:11434"
        )
        
        print(f"✅ LiteLLM hoạt động!")
        print(f"📝 Response: {response.choices[0].message.content[:500]}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi LiteLLM: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_extract_thinker_classify(file_path: str):
    """Test phân loại với extract_thinker"""
    print("\n" + "=" * 60)
    print("🔍 TEST EXTRACT_THINKER CLASSIFY")
    print("=" * 60)
    
    try:
        from extract_thinker import (
            Extractor,
            Classification,
            DocumentLoaderGoogleDocumentAI,
            GoogleDocAIConfig,
        )
        
        # Setup
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        config = GoogleDocAIConfig(
            project_id=os.getenv("DOCUMENTAI_PROJECT_ID"),
            location=os.getenv("DOCUMENTAI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENTAI_PROCESSOR_ID"),
            credentials=os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        )
        
        extractor = Extractor()
        extractor.load_document_loader(DocumentLoaderGoogleDocumentAI(config))
        extractor.load_llm("ollama/qwen2.5:3b")
        
        print(f"📁 File: {file_path}")
        print(f"🤖 Model: ollama/qwen2.5:3b")
        
        # Classifications đơn giản
        classifications = [
            Classification(name="identity", description="Giấy tờ tùy thân: CCCD, hộ chiếu, giấy khai sinh"),
            Classification(name="vehicle", description="Giấy tờ phương tiện: bằng lái, đăng ký xe"),
            Classification(name="finance", description="Giấy tờ tài chính: hóa đơn, biên lai, hợp đồng"),
        ]
        
        print("\n⏳ Đang phân loại...")
        result = extractor.classify(file_path, classifications)
        
        print(f"\n✅ Phân loại thành công!")
        print(f"📌 Kết quả: {result}")
        print(f"📌 Name: {getattr(result, 'name', 'N/A')}")
        print(f"📌 Confidence: {getattr(result, 'confidence', 'N/A')}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Lỗi: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_extract_thinker_extract(file_path: str):
    """Test trích xuất với extract_thinker"""
    print("\n" + "=" * 60)
    print("📋 TEST EXTRACT_THINKER EXTRACT")
    print("=" * 60)
    
    try:
        from extract_thinker import (
            Extractor,
            DocumentLoaderGoogleDocumentAI,
            GoogleDocAIConfig,
        )
        from pydantic import BaseModel, Field
        from typing import Optional
        
        # Contract đơn giản
        class SimpleContract(BaseModel):
            """Thông tin cơ bản từ văn bản"""
            ten: Optional[str] = Field(None, description="Họ và tên")
            so_giay_to: Optional[str] = Field(None, description="Số CCCD/CMND/Hộ chiếu")
            ngay_sinh: Optional[str] = Field(None, description="Ngày tháng năm sinh")
        
        # Setup
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        config = GoogleDocAIConfig(
            project_id=os.getenv("DOCUMENTAI_PROJECT_ID"),
            location=os.getenv("DOCUMENTAI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENTAI_PROCESSOR_ID"),
            credentials=os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        )
        
        extractor = Extractor()
        extractor.load_document_loader(DocumentLoaderGoogleDocumentAI(config))
        extractor.load_llm("ollama/qwen2.5:3b")
        
        print(f"📁 File: {file_path}")
        print(f"🤖 Model: ollama/qwen2.5:3b")
        
        print("\n⏳ Đang trích xuất...")
        result = extractor.extract(file_path, SimpleContract)
        
        print(f"\n✅ Trích xuất thành công!")
        print(f"📌 Kết quả: {result}")
        if result:
            print(f"📌 Data: {result.model_dump()}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Lỗi: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys
    
    print("🚀 KIỂM TRA SUY LUẬN (INFERENCE)")
    print("=" * 60)
    
    # Test 1: Ollama trực tiếp
    if not test_ollama_direct():
        print("\n⚠️ Ollama không hoạt động!")
        sys.exit(1)
    
    # Test 2: LiteLLM
    test_litellm()
    
    # Test 3 & 4: Extract Thinker (nếu có file)
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            test_extract_thinker_classify(file_path)
            test_extract_thinker_extract(file_path)
        else:
            print(f"\n❌ File không tồn tại: {file_path}")
    else:
        print("\n💡 Để test với file, chạy: python test_inference.py <file_path>")
