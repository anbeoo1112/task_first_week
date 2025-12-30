"""
Tạo Ground Truth từ API output + Script đánh giá.

Bước 1: Chạy create_ground_truth() để tạo draft ground truth
Bước 2: Review và sửa thủ công các file JSON trong ground_truth/
Bước 3: Chạy evaluate() để đánh giá API
"""
import os
import json
from pathlib import Path
from core.pipeline import DocumentProcessor

DATASET_DIR = "dataset"


def create_ground_truth():
    """Chạy API và tạo draft ground truth cho từng ảnh."""
    processor = DocumentProcessor()
    
    for category in Path(DATASET_DIR).iterdir():
        if not category.is_dir():
            continue
        for doc_type in category.iterdir():
            if not doc_type.is_dir():
                continue
            
            images_dir = doc_type / "images"
            gt_dir = doc_type / "ground_truth"
            
            if not images_dir.exists():
                continue
            
            # Ensure ground_truth directory exists
            gt_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n📂 {doc_type}")
            
            for img_file in images_dir.iterdir():
                if img_file.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.pdf'}:
                    continue
                
                gt_file = gt_dir / f"{img_file.stem}.json"
                
                # Skip nếu đã có ground truth
                if gt_file.exists():
                    print(f"  ⏭️ {img_file.name} (đã có GT)")
                    continue
                
                print(f"  🔄 {img_file.name}...", end=" ")
                
                try:
                    result = processor.run(str(img_file))
                    doc = result.get("documents", [{}])[0] if result.get("documents") else {}
                    
                    # Lưu ground truth
                    gt_data = {
                        "_file": img_file.name,
                        "_doc_type": doc.get("docType"),
                        "expected": doc.get("data", {})
                    }
                    with open(gt_file, "w", encoding="utf-8") as f:
                        json.dump(gt_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ -> {gt_file.name}")
                    
                except Exception as e:
                    print(f"❌ {str(e)[:50]}")


def evaluate():
    """So sánh API output với Ground Truth."""
    processor = DocumentProcessor()
    results = []
    
    for category in Path(DATASET_DIR).iterdir():
        if not category.is_dir():
            continue
        for doc_type in category.iterdir():
            if not doc_type.is_dir():
                continue
            
            images_dir = doc_type / "images"
            gt_dir = doc_type / "ground_truth"
            
            if not images_dir.exists() or not gt_dir.exists():
                continue
            
            for gt_file in gt_dir.glob("*.json"):
                img_file = images_dir / f"{gt_file.stem}.jpeg"
                if not img_file.exists():
                    img_file = images_dir / f"{gt_file.stem}.jpg"
                if not img_file.exists():
                    img_file = images_dir / f"{gt_file.stem}.png"
                if not img_file.exists():
                    continue
                
                # Load ground truth
                with open(gt_file, encoding="utf-8") as f:
                    gt = json.load(f)
                expected = gt.get("expected", {})
                
                # Chạy API
                result = processor.run(str(img_file))
                doc = result.get("documents", [{}])[0] if result.get("documents") else {}
                actual = doc.get("data", {})
                
                # So sánh từng trường
                total_fields = len(expected)
                matched = 0
                for key, exp_val in expected.items():
                    act_val = actual.get(key)
                    if str(exp_val).strip().lower() == str(act_val).strip().lower():
                        matched += 1
                
                accuracy = (matched / total_fields * 100) if total_fields > 0 else 0
                
                results.append({
                    "file": str(img_file),
                    "doc_type": gt.get("_doc_type"),
                    "total_fields": total_fields,
                    "matched": matched,
                    "accuracy": round(accuracy, 1)
                })
                
                print(f"📊 {img_file.name}: {matched}/{total_fields} ({accuracy:.1f}%)")
    
    # Tổng kết
    if results:
        avg = sum(r["accuracy"] for r in results) / len(results)
        print(f"\n{'='*50}")
        print(f"📈 Tổng: {len(results)} files | Accuracy trung bình: {avg:.1f}%")
        
        # Lưu report
        with open("evaluation_report.json", "w", encoding="utf-8") as f:
            json.dump({"average_accuracy": avg, "details": results}, f, ensure_ascii=False, indent=2)
        print(f"📄 Report: evaluation_report.json")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        evaluate()
    else:
        print("Tạo Ground Truth từ API...")
        create_ground_truth()
        print("\n⚠️ Hãy review và sửa các file ground_truth/*.json")
        print("Sau đó chạy: python evaluate_dataset.py eval")
