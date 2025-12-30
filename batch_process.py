"""
Xử lý batch images từ folder 'image/' và xuất kết quả ra 'output/results.json'.
"""
import os
import json
import time
from pathlib import Path
from core.pipeline import DocumentProcessor

INPUT_DIR = "image"
OUTPUT_FILE = "output/results.json"

def main():
    processor = DocumentProcessor()
    results = []
    
    # Tạo output folder
    Path("output").mkdir(exist_ok=True)
    
    # Duyệt tất cả file ảnh
    for root, dirs, files in os.walk(INPUT_DIR):
        for filename in files:
            file_path = Path(root) / filename
            if file_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.pdf'}:
                continue
            
            print(f"🔄 {file_path}...", end=" ")
            start = time.time()
            
            try:
                result = processor.run(str(file_path))
                elapsed = time.time() - start
                
                # Thêm metadata
                doc = result.get("documents", [{}])[0] if result.get("documents") else {}
                results.append({
                    "input": str(file_path),
                    "category": doc.get("category"),
                    "docType": doc.get("docType"),
                    "data": doc.get("data"),
                    "confidence": doc.get("confidence"),
                    "time_sec": round(elapsed, 2),
                    "error": result.get("error")
                })
                print(f"✅ {doc.get('docType', '?')} ({elapsed:.1f}s)")
                
            except Exception as e:
                results.append({
                    "input": str(file_path),
                    "error": str(e)[:100]
                })
                print(f"❌ {str(e)[:50]}")
    
    # Lưu tất cả vào 1 file JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"total": len(results), "results": results}, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Đã xử lý {len(results)} files. Kết quả: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
