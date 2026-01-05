import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from extract_thinker import Extractor, Contract, Process
from contracts.vehicle.driver_license import VietnamDriverLicense as DriverLicense
# from contracts.identity.student_card import VietnamStudentCard
from extract_thinker.utils import get_file_extension

load_dotenv()

# --- Configuration ---
# Chọn loại contract cần test
TEST_CONTRACT = DriverLicense
# TEST_CONTRACT = VietnamStudentCard

# Thư mục chứa các file text đã OCR (cần khớp với loại contract)
# SOURCE_DIR = "benchmark_results/identity_student_card"
SOURCE_DIR = "benchmark_results/vehicle_driver_license" 

OUTPUT_FILE = "benchmark_prompt_vs_tool_report.json"
MAX_FILES = 20  # Giới hạn số file để test cho nhanh

def load_text_content(file_path: str) -> str:
    """Đọc nội dung file text"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def run_extraction(extractor, content: str, is_dynamic: bool) -> Dict[str, Any]:
    """Chạy trích xuất với chế độ dynamic (prompt) hoặc tool"""
    
    # Configure Extractor mode
    # is_dynamic=True  -> Prompt Engineering (JSON Schema injection)
    # is_dynamic=False -> Tool/Function Calling
    if hasattr(extractor.llm, 'is_dynamic'): # Check if LLM supports this flag directly (some custom implementations might)
         # Note: In ExtractThinker, usually we set this via the LLM object passed to Extractor
         pass

    # Modify the internal LLM state to switch modes
    # This is a bit of a hack depending on how ExtractThinker is instantiated, 
    # but based on the codebase, the LLM object holds the `is_dynamic` state.
    extractor.llm.is_dynamic = is_dynamic
    
    start_time = time.time()
    try:
        # We manually process here to avoid the whole pipeline overhead 
        # and strictly test the LLM extraction part.
        
        # In `process.py`, extract() calls extractor.extract(pages, contract)
        # We will simulate a simple page structure
        pages = [{"content": content}]
        
        result = extractor.extract(pages, TEST_CONTRACT)
        
        duration_ms = (time.time() - start_time) * 1000
        return {
            "success": True,
            "time_ms": round(duration_ms, 2),
            "data": result.model_dump() if result else None
        }
    except Exception as e:
        print(f"    ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        duration_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "time_ms": round(duration_ms, 2),
            "error": str(e)
        }

def main():
    print(f"🚀 Starting Benchmark: Prompt vs Tool")
    print(f"📄 Contract: {TEST_CONTRACT.__name__}")
    print(f"📂 Source: {SOURCE_DIR}")
    
    # Setup Extractor with a standard model
    from extract_thinker import Extractor, LLM, DocumentLoaderTxt
    
    # Initialize LLM - Adjust model as needed
    llm = LLM(model="gemini/gemini-2.0-flash") 
    extractor = Extractor(llm=llm) 
    extractor.load_document_loader(DocumentLoaderTxt())

    results = []
    
    source_path = Path(SOURCE_DIR)
    if not source_path.exists():
        print(f"❌ Error: Directory {SOURCE_DIR} not found!")
        return

    files = list(source_path.glob("*.txt"))[:MAX_FILES]
    print(f"📊 Found {len(files)} files to process.\n")

    for idx, file_path in enumerate(files):
        print(f"[{idx+1}/{len(files)}] Processing {file_path.name}...")
        content = load_text_content(str(file_path))
        
        # Run Prompt Mode
        print("  - Running Prompt Mode...", end=" ", flush=True)
        res_prompt = run_extraction(extractor, content, is_dynamic=True)
        print(f"{'✅' if res_prompt['success'] else '❌'} {res_prompt['time_ms']}ms")

        # Run Tool Mode
        print("  - Running Tool Mode...", end=" ", flush=True)
        res_tool = run_extraction(extractor, content, is_dynamic=False)
        print(f"{'✅' if res_tool['success'] else '❌'} {res_tool['time_ms']}ms")
        
        results.append({
            "file": file_path.name,
            "prompt_mode": res_prompt,
            "tool_mode": res_tool
        })

    # Save Report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Benchmark completed! Results saved to {OUTPUT_FILE}")
    
    # Quick Statistics
    success_prompt = sum(1 for r in results if r['prompt_mode']['success'])
    success_tool = sum(1 for r in results if r['tool_mode']['success'])
    avg_time_prompt = sum(r['prompt_mode']['time_ms'] for r in results if r['prompt_mode']['success']) / max(success_prompt, 1)
    avg_time_tool = sum(r['tool_mode']['time_ms'] for r in results if r['tool_mode']['success']) / max(success_tool, 1)
    
    print("\n📊 Summary:")
    print(f"Mode      | Success Rate | Avg Time (ms)")
    print(f"----------|--------------|--------------")
    print(f"Prompt    | {success_prompt}/{len(files)}        | {avg_time_prompt:.0f}")
    print(f"Tool      | {success_tool}/{len(files)}        | {avg_time_tool:.0f}")

if __name__ == "__main__":
    main()
