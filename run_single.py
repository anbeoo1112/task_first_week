from core.pipeline import DocumentProcessor
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_single.py <file_path>")
        sys.exit(1)
        
    path = sys.argv[1]
    processor = DocumentProcessor()
    result = processor.run(path)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
