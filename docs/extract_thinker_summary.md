# ExtractThinker - Tóm tắt nhanh

## 1. Document Loaders
**Đọc và chuyển đổi file thành text cho LLM**

| Loader | Dùng cho | Chi phí |
|--------|----------|---------|
| `DocumentLoaderGoogleDocumentAI` | PDF scan, ảnh, chữ viết tay | ~$0.0015/trang |
| `DocumentLoaderPyPdf` | PDF text-based (từ Word) | Free |
| `DocumentLoaderMarkItDown` | Office, HTML, JSON, CSV... | Free |
| `DocumentLoaderTesseract` | OCR local | Free |

---

## 2. Contracts
**Schema dữ liệu trích xuất (Pydantic)**

```python
class Invoice(Contract):
    invoice_number: str = Field(description="Số hóa đơn")
    total: float = Field(description="Tổng tiền")
```

---

## 3. Extractor
**Component chính: classify + extract**

```python
extractor = Extractor()
extractor.load_document_loader(loader)
extractor.load_llm("gemini/gemini-2.0-flash")

result = extractor.classify(file, classifications)   # Phân loại
data = extractor.extract(file, Contract, vision=True) # Trích xuất
```

---

## 4. Classification
**4 kỹ thuật phân loại**

| Kỹ thuật | Mô tả |
|----------|-------|
| **Basic** | 1 LLM, danh sách `Classification` |
| **Tree** | Phân cấp (nhóm → loại cụ thể) |
| **MoM** | Nhiều model song song, voting |
| **Vision** | `vision=True` - LLM nhìn ảnh |

---

## 5. Completion Strategies
**Xử lý tài liệu lớn**

| Strategy | Khi nào dùng |
|----------|--------------|
| `FORBIDDEN` | Tài liệu nhỏ (mặc định) |
| `CONCATENATE` | Vừa phải, context lớn |
| `PAGINATE` | Lớn, xử lý từng trang |

---

## 6. LLM Integration
**Kết nối với LLM providers**

```python
llm = LLM("gpt-4o")                      # OpenAI
llm = LLM("claude-3-5-sonnet-20241022")  # Anthropic
llm = LLM("gemini/gemini-2.0-flash")     # Google
llm = LLM("ollama/llama3.2")             # Local
```

**Tính năng:** Thinking mode, Router fallback, Dynamic parsing

---

## 7. Evals
**Đánh giá độ chính xác**

- Field-level metrics (Precision, Recall, F1)
- Hallucination detection
- Cost tracking
