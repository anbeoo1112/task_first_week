"""
Benchmark OCR với Google Document AI - Full Version

Đánh giá:
1. Thời gian xử lý
2. Số trang
3. Độ chính xác trích xuất (so sánh với filename pattern)
4. Chất lượng tiếng Việt (số ký tự có dấu)
5. Lưu text OCR ra file
"""
import os
import sys
import time
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from dotenv import load_dotenv

load_dotenv()

@dataclass
class OCRResult:
    """Kết quả OCR cho 1 file"""
    file_path: str
    file_name: str
    category: str
    file_size_kb: float
    num_pages: int
    processing_time_ms: float
    text_length: int
    vietnamese_chars: int
    vietnamese_ratio: float
    extracted_so_hieu: Optional[str]
    filename_pattern: Optional[str]  
    pattern_match: bool
    ocr_text_file: Optional[str] = None
    error: Optional[str] = None

@dataclass
class BenchmarkSummary:
    """Tổng hợp kết quả benchmark"""
    total_files: int
    success_count: int
    error_count: int
    total_pages: int
    avg_time_per_page_ms: float
    avg_time_per_file_ms: float
    pattern_match_rate: float
    avg_vietnamese_ratio: float
    total_time_seconds: float
    files_per_category: Dict[str, int]

class DocumentAIOCRBenchmark:
    def __init__(self, output_dir: str = "benchmark_results"):
        self.results: List[OCRResult] = []
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self._setup_loader()
    
    def _setup_loader(self):
        """Setup Document AI loader"""
        from extract_thinker import DocumentLoaderGoogleDocumentAI, GoogleDocAIConfig
        
        project_id = os.getenv("DOCUMENTAI_PROJECT_ID")
        location = os.getenv("DOCUMENTAI_LOCATION", "us")
        processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
        credentials_path = os.getenv("DOCUMENTAI_GOOGLE_CREDENTIALS", "credentials.json")
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        config = GoogleDocAIConfig(
            project_id=project_id,
            location=location,
            processor_id=processor_id,
            credentials=credentials_path
        )
        self.loader = DocumentLoaderGoogleDocumentAI(config)
        print(f"✅ Document AI configured: {project_id}/{processor_id}")
    
    def _extract_so_hieu_from_text(self, text: str) -> Optional[str]:
        """Trích xuất số hiệu từ text OCR"""
        patterns = [
            r'Số:\s*(\d+[-/]\w+[-/]\w+)',
            r'Số:\s*(\d+[-/]\d+[-/]\w+[-/]\w+)',
            r'(\d+[-/]\d+[-/]QĐ[-/](?:TTg|UBND))',
            r'(\d+[-/]VBHN[-/]\w+)',
            r'(\d+[-/]NQ[-/]CP)',
            r'(\d+[-/](?:CD|CT)[-/]TTg)',
            r'(\d+[-/]TB[-/]VPCP)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_pattern_from_filename(self, filename: str) -> Optional[str]:
        """Trích xuất pattern từ tên file"""
        name = filename.replace('.pdf', '').replace('.PDF', '')
        return name
    
    def _count_vietnamese_chars(self, text: str) -> int:
        """Đếm số ký tự tiếng Việt có dấu"""
        vn_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
        vn_chars += vn_chars.upper()
        return sum(1 for c in text if c in vn_chars)
    
    def _save_ocr_text(self, file_name: str, category: str, text: str) -> str:
        """Lưu text OCR ra file"""
        cat_dir = self.output_dir / category
        cat_dir.mkdir(exist_ok=True)
        
        txt_file = cat_dir / f"{Path(file_name).stem}.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        return str(txt_file)
    
    def ocr_file(self, file_path: str, category: str) -> OCRResult:
        """OCR một file và trả về kết quả"""
        file_name = os.path.basename(file_path)
        file_size_kb = os.path.getsize(file_path) / 1024
        
        try:
            start_time = time.time()
            pages = self.loader.load(file_path)
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Combine all pages
            if isinstance(pages, list):
                num_pages = len(pages)
                full_text = "\n".join(
                    p.get("content", "") if isinstance(p, dict) else str(p) 
                    for p in pages
                )
            else:
                num_pages = 1
                full_text = str(pages)
            
            text_length = len(full_text)
            vn_chars = self._count_vietnamese_chars(full_text)
            vn_ratio = vn_chars / max(text_length, 1)
            
            extracted_so_hieu = self._extract_so_hieu_from_text(full_text)
            filename_pattern = self._extract_pattern_from_filename(file_name)
            
            # Check pattern match
            pattern_match = False
            if extracted_so_hieu and filename_pattern:
                norm_extracted = extracted_so_hieu.replace('/', '-').replace('_', '-').lower()
                norm_filename = filename_pattern.replace('/', '-').replace('_', '-').lower()
                pattern_match = norm_extracted in norm_filename or norm_filename in norm_extracted
            
            # Save OCR text
            ocr_text_file = self._save_ocr_text(file_name, category, full_text)
            
            return OCRResult(
                file_path=file_path,
                file_name=file_name,
                category=category,
                file_size_kb=round(file_size_kb, 2),
                num_pages=num_pages,
                processing_time_ms=round(processing_time_ms, 2),
                text_length=text_length,
                vietnamese_chars=vn_chars,
                vietnamese_ratio=round(vn_ratio, 4),
                extracted_so_hieu=extracted_so_hieu,
                filename_pattern=filename_pattern,
                pattern_match=pattern_match,
                ocr_text_file=ocr_text_file
            )
            
        except Exception as e:
            return OCRResult(
                file_path=file_path,
                file_name=file_name,
                category=category,
                file_size_kb=round(file_size_kb, 2),
                num_pages=0,
                processing_time_ms=0,
                text_length=0,
                vietnamese_chars=0,
                vietnamese_ratio=0,
                extracted_so_hieu=None,
                filename_pattern=self._extract_pattern_from_filename(file_name),
                pattern_match=False,
                error=str(e)[:100]
            )
    
    def run_benchmark(self, dataset_path: str, max_files: int = 100) -> BenchmarkSummary:
        """Chạy benchmark trên dataset"""
        print(f"\n{'='*60}")
        print(f"🚀 BẮT ĐẦU BENCHMARK OCR - FULL DATASET")
        print(f"{'='*60}")
        print(f"📁 Dataset: {dataset_path}")
        print(f"📊 Max files per category: {max_files}")
        print(f"📂 Output dir: {self.output_dir}")
        
        dataset = Path(dataset_path)
        if not dataset.exists():
            raise ValueError(f"Dataset path không tồn tại: {dataset_path}")
        
        # Collect all files by category
        files_by_category = {}
        
        # Government documents
        gov_folders = {
            "Van_ban_chi_dao_dieu_hanh": "van_ban_chi_dao",
            "Van_ban_quy_pham_phap_luat/Quyet_dinh": "quyet_dinh",
            "Van_ban_quy_pham_phap_luat/Nghi_dinh": "nghi_dinh",
            "Van_ban_quy_pham_phap_luat/Thong_tu": "thong_tu",
            "Van_ban_quy_pham_phap_luat/Luat_-_Phap_lenh": "luat_phap_lenh",
            "Nghi_quyet_cua_Chinh_phu": "nghi_quyet_cp",
            "Nghi_quyet_phien_hop_cua_Chinh_phu": "nghi_quyet_phien_hop",
            "Van_ban_hop_nhat": "van_ban_hop_nhat",
        }
        
        for folder, category in gov_folders.items():
            folder_path = dataset / folder
            if folder_path.exists():
                pdfs = list(folder_path.glob("*.pdf"))[:max_files]
                if pdfs:
                    files_by_category[category] = pdfs
                    print(f"  📂 {category}: {len(pdfs)} files")
        
        # Identity, Vehicle, Finance
        for main_cat in ["identity", "vehicle", "finance"]:
            cat_path = dataset / main_cat
            if cat_path.exists():
                for subcat in cat_path.iterdir():
                    if subcat.is_dir():
                        images_path = subcat / "images"
                        if images_path.exists():
                            files = list(images_path.glob("*"))[:max_files]
                            if files:
                                category_name = f"{main_cat}_{subcat.name}"
                                files_by_category[category_name] = files
                                print(f"  📂 {category_name}: {len(files)} files")
        
        total_files = sum(len(f) for f in files_by_category.values())
        print(f"\n📊 Tổng số files để benchmark: {total_files}")
        print(f"{'='*60}\n")
        
        # Run OCR on each file
        start_total = time.time()
        self.results = []
        processed = 0
        
        for category, files in files_by_category.items():
            print(f"\n📁 Category: {category}")
            print("-" * 40)
            
            for file_path in files:
                processed += 1
                print(f"[{processed}/{total_files}] 🔄 {file_path.name}...", end=" ", flush=True)
                result = self.ocr_file(str(file_path), category)
                self.results.append(result)
                
                if result.error:
                    print(f"❌ {result.error[:30]}")
                else:
                    match_icon = "✅" if result.pattern_match else "⚠️"
                    print(f"✅ {result.num_pages}p {result.processing_time_ms:.0f}ms VN:{result.vietnamese_ratio:.0%} {match_icon}")
        
        total_time = time.time() - start_total
        
        # Calculate summary
        success_results = [r for r in self.results if not r.error]
        error_results = [r for r in self.results if r.error]
        
        total_pages = sum(r.num_pages for r in success_results)
        total_time_ms = sum(r.processing_time_ms for r in success_results)
        
        summary = BenchmarkSummary(
            total_files=len(self.results),
            success_count=len(success_results),
            error_count=len(error_results),
            total_pages=total_pages,
            avg_time_per_page_ms=round(total_time_ms / max(total_pages, 1), 2),
            avg_time_per_file_ms=round(total_time_ms / max(len(success_results), 1), 2),
            pattern_match_rate=round(sum(1 for r in success_results if r.pattern_match) / max(len(success_results), 1), 4),
            avg_vietnamese_ratio=round(sum(r.vietnamese_ratio for r in success_results) / max(len(success_results), 1), 4),
            total_time_seconds=round(total_time, 2),
            files_per_category={cat: len([r for r in self.results if r.category == cat]) for cat in files_by_category}
        )
        
        return summary
    
    def print_report(self, summary: BenchmarkSummary):
        """In báo cáo benchmark"""
        print(f"\n{'='*60}")
        print(f"📊 BÁO CÁO BENCHMARK OCR - DOCUMENT AI")
        print(f"{'='*60}")
        
        print(f"""
┌─────────────────────────────────────────────────────────┐
│ TỔNG QUAN                                               │
├─────────────────────────────────────────────────────────┤
│ Tổng số files:          {summary.total_files:>10}                      │
│ Thành công:             {summary.success_count:>10}                      │
│ Lỗi:                    {summary.error_count:>10}                      │
│ Tổng số trang:          {summary.total_pages:>10}                      │
│ Thời gian tổng:         {summary.total_time_seconds:>10.1f}s                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ HIỆU SUẤT                                               │
├─────────────────────────────────────────────────────────┤
│ Thời gian TB/trang:     {summary.avg_time_per_page_ms:>10.0f}ms                    │
│ Thời gian TB/file:      {summary.avg_time_per_file_ms:>10.0f}ms                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CHẤT LƯỢNG OCR                                          │
├─────────────────────────────────────────────────────────┤
│ Pattern match rate:     {summary.pattern_match_rate*100:>10.1f}%                    │
│ Vietnamese char ratio:  {summary.avg_vietnamese_ratio*100:>10.1f}%                    │
└─────────────────────────────────────────────────────────┘
""")
        
        # Per category stats
        print("📊 THEO CATEGORY:")
        for cat, count in summary.files_per_category.items():
            cat_results = [r for r in self.results if r.category == cat and not r.error]
            if cat_results:
                match_rate = sum(1 for r in cat_results if r.pattern_match) / len(cat_results)
                avg_vn = sum(r.vietnamese_ratio for r in cat_results) / len(cat_results)
                print(f"  {cat:30} | {count:3} files | Match: {match_rate*100:5.1f}% | VN: {avg_vn*100:5.1f}%")
        
        # Errors
        errors = [r for r in self.results if r.error]
        if errors:
            print(f"\n⚠️ FILES LỖI ({len(errors)}):")
            for r in errors[:10]:
                print(f"  - {r.file_name}: {r.error}")
    
    def save_report(self, summary: BenchmarkSummary, output_path: str = "benchmark_ocr_report.json"):
        """Lưu báo cáo ra file JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": asdict(summary),
            "details": [asdict(r) for r in self.results]
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Báo cáo JSON: {output_path}")
        print(f"📂 OCR text files: {self.output_dir}/")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark OCR với Document AI")
    parser.add_argument("--dataset", default="dataset", help="Đường dẫn dataset")
    parser.add_argument("--max-files", type=int, default=100, help="Số files tối đa mỗi category")
    parser.add_argument("--output", default="benchmark_ocr_report.json", help="File output JSON")
    parser.add_argument("--output-dir", default="benchmark_results", help="Thư mục lưu text OCR")
    
    args = parser.parse_args()
    
    benchmark = DocumentAIOCRBenchmark(output_dir=args.output_dir)
    summary = benchmark.run_benchmark(args.dataset, max_files=args.max_files)
    benchmark.print_report(summary)
    benchmark.save_report(summary, args.output)


if __name__ == "__main__":
    main()
