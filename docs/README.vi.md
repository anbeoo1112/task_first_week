<p align="center">
  <img src="https://github.com/enoch3712/Open-DocLLM/assets/9283394/41d9d151-acb5-44da-9c10-0058f76c2512" alt="Extract Thinker Logo" width="200"/> 
</p>
<p align="center">
<img alt="Python Version" src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" />
<a href="https://medium.com/@enoch3712">
    <img alt="Medium" src="https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white" />
</a>
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/enoch3712/Open-DocLLM" />
<img alt="Github License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" />
</p>

# ExtractThinker

ExtractThinker là một công cụ xử lý thông minh tài liệu linh hoạt, tận dụng các mô hình ngôn ngữ lớn (LLM) để trích xuất và phân loại dữ liệu có cấu trúc từ tài liệu, hoạt động giống như một ORM cho các quy trình xử lý tài liệu liền mạch.

**TL;DR: Xử lý thông minh tài liệu dành cho LLM**

## 🚀 Tính năng chính

- **Trình tải tài liệu linh hoạt**: Hỗ trợ nhiều trình tải tài liệu, bao gồm Tesseract OCR, Azure Form Recognizer, AWS Textract, Google Document AI, và nhiều hơn nữa.
- **Contract tùy chỉnh**: Xác định các contract trích xuất tùy chỉnh bằng cách sử dụng các mô hình Pydantic để trích xuất dữ liệu chính xác.
- **Phân loại nâng cao**: Phân loại tài liệu hoặc các phần của tài liệu bằng cách sử dụng các chiến lược và phân loại tùy chỉnh.
- **Xử lý bất đồng bộ**: Sử dụng xử lý bất đồng bộ để xử lý hiệu quả các tài liệu lớn.
- **Hỗ trợ đa định dạng**: Làm việc liền mạch với nhiều định dạng tài liệu khác nhau như PDF, hình ảnh, bảng tính, v.v.
- **Tương tác kiểu ORM**: Tương tác với tài liệu và LLM theo phong cách giống như ORM để phát triển trực quan.
- **Chiến lược chia nhỏ**: Triển khai các chiến lược chia nhỏ (lazy hoặc eager) để xử lý tài liệu theo từng trang hoặc toàn bộ.
- **Tích hợp với các LLM**: Dễ dàng tích hợp với các nhà cung cấp LLM khác nhau như OpenAI, Anthropic, Cohere, v.v.
- **Phát triển dựa vào cộng đồng**: Lấy cảm hứng từ hệ sinh thái LangChain với trọng tâm là xử lý tài liệu thông minh.
![image](https://github.com/user-attachments/assets/844b425c-0bb7-4abc-9d08-96e4a736d096)

## 📦 Cài đặt

Cài đặt ExtractThinker bằng pip:

```bash
pip install extract_thinker
```

## 🛠️ Sử dụng

### Ví dụ trích xuất cơ bản

Dưới đây là một ví dụ nhanh để bạn bắt đầu với ExtractThinker. Ví dụ này minh họa cách tải một tài liệu bằng PyPdf và trích xuất các trường cụ thể được xác định trong một contract.

```python
import os
from dotenv import load_dotenv
from extract_thinker import Extractor, DocumentLoaderPyPdf, Contract

load_dotenv()

class InvoiceContract(Contract):
    invoice_number: str
    invoice_date: str

# Đặt đường dẫn đến tệp thực thi Tesseract của bạn
test_file_path = os.path.join("path_to_your_files", "invoice.pdf")

# Khởi tạo extractor
extractor = Extractor()
extractor.load_document_loader(DocumentLoaderPyPdf())
extractor.load_llm("gpt-4o-mini")  # hoặc bất kỳ mô hình được hỗ trợ nào khác

# Trích xuất dữ liệu từ tài liệu
result = extractor.extract(test_file_path, InvoiceContract)

print("Invoice Number:", result.invoice_number)
print("Invoice Date:", result.invoice_date)
```

### Ví dụ phân loại

ExtractThinker cho phép bạn phân loại tài liệu hoặc các phần của tài liệu bằng cách sử dụng các phân loại tùy chỉnh:

```python
import os
from dotenv import load_dotenv
from extract_thinker import (
    Extractor, Classification, Process, ClassificationStrategy,
    DocumentLoaderPyPdf, Contract
)

load_dotenv()

class InvoiceContract(Contract):
    invoice_number: str
    invoice_date: str

class DriverLicenseContract(Contract):
    name: str
    license_number: str

# Khởi tạo extractor và tải trình tải tài liệu
extractor = Extractor()
extractor.load_document_loader(DocumentLoaderPyPdf())
extractor.load_llm("gpt-4o-mini")

# Định nghĩa các phân loại
classifications = [
    Classification(
        name="Invoice",
        description="An invoice document",
        contract=InvoiceContract,
        extractor=extractor,
    ),
    Classification(
        name="Driver License",
        description="A driver's license document",
        contract=DriverLicenseContract,
        extractor=extractor,
    ),
]

# Phân loại tài liệu trực tiếp bằng extractor
result = extractor.classify(
    "path_to_your_document.pdf",  # Có thể là đường dẫn tệp hoặc luồng IO
    classifications,
    image=True  # Đặt là True để phân loại dựa trên hình ảnh
)

# Kết quả sẽ là một đối tượng ClassificationResponse với các trường 'name' và 'confidence'
print(f"Document classified as: {result.name}")
print(f"Confidence level: {result.confidence}")
```

### Ví dụ chia nhỏ tệp

ExtractThinker cho phép bạn chia nhỏ và xử lý tài liệu bằng các chiến lược khác nhau. Dưới đây là cách bạn có thể chia tài liệu và trích xuất dữ liệu dựa trên phân loại.

```python
import os
from dotenv import load_dotenv
from extract_thinker import (
    Extractor,
    Process,
    Classification,
    ImageSplitter,
    DocumentLoaderTesseract,
    Contract,
    SplittingStrategy,
)

load_dotenv()

class DriverLicenseContract(Contract):
    name: str
    license_number: str

class InvoiceContract(Contract):
    invoice_number: str
    invoice_date: str

# Khởi tạo extractor và tải trình tải tài liệu
extractor = Extractor()
extractor.load_document_loader(DocumentLoaderPyPdf())
extractor.load_llm("gpt-4o-mini")

# Định nghĩa các phân loại
classifications = [
    Classification(
        name="Driver License",
        description="A driver's license document",
        contract=DriverLicenseContract,
        extractor=extractor,
    ),
    Classification(
        name="Invoice",
        description="An invoice document",
        contract=InvoiceContract,
        extractor=extractor,
    ),
]

# Khởi tạo process và tải splitter
process = Process()
process.load_document_loader(DocumentLoaderPyPdf())
process.load_splitter(ImageSplitter(model="gpt-4o-mini"))

# Tải và xử lý tài liệu
path_to_document = "path_to_your_multipage_document.pdf"
split_content = (
    process.load_file(path_to_document)
    .split(classifications, strategy=SplittingStrategy.LAZY)
    .extract()
)

# Xử lý nội dung đã trích xuất khi cần thiết
for item in split_content:
    if isinstance(item, InvoiceContract):
        print("Extracted Invoice:")
        print("Invoice Number:", item.invoice_number)
        print("Invoice Date:", item.invoice_date)
    elif isinstance(item, DriverLicenseContract):
        print("Extracted Driver License:")
        print("Name:", item.name)
        print("License Number:", item.license_number)

```

### Ví dụ xử lý hàng loạt

Bạn cũng có thể thực hiện xử lý hàng loạt các tài liệu:

```python
from extract_thinker import Extractor, Contract

class ReceiptContract(Contract):
    store_name: str
    total_amount: float

extractor = Extractor()
extractor.load_llm("gpt-4o-mini")

# Danh sách các đường dẫn tệp hoặc luồng
document = "receipt1.jpg"

batch_job = extractor.extract_batch(
    source=document,
    response_model=ReceiptContract,
    vision=True,
)

# Theo dõi trạng thái công việc hàng loạt
print("Batch Job Status:", await batch_job.get_status())

# Lấy kết quả khi quá trình xử lý hoàn tất
results = await batch_job.get_result()
for result in results.parsed_results:
    print("Store Name:", result.store_name)
    print("Total Amount:", result.total_amount)
```

### Ví dụ tích hợp LLM cục bộ

ExtractThinker hỗ trợ tích hợp LLM tùy chỉnh. Dưới đây là cách bạn có thể sử dụng một LLM tùy chỉnh:

```python
from extract_thinker import Extractor, LLM, DocumentLoaderTesseract, Contract

class InvoiceContract(Contract):
    invoice_number: str
    invoice_date: str

# Khởi tạo extractor
extractor = Extractor()
extractor.load_document_loader(DocumentLoaderTesseract(os.getenv("TESSERACT_PATH")))

# Tải một LLM tùy chỉnh (ví dụ: Ollama)
os.environ['API_BASE'] = "http://localhost:11434"
llm = LLM('ollama/phi3')
extractor.load_llm(llm)

# Trích xuất dữ liệu
result = extractor.extract("invoice.png", InvoiceContract)
print("Invoice Number:", result.invoice_number)
print("Invoice Date:", result.invoice_date)
```

## 📚 Tài liệu và Tài nguyên

- **Ví dụ**: Kiểm tra thư mục examples để xem các Jupyter notebook và script minh họa các trường hợp sử dụng khác nhau.
- **Bài viết Medium**: Đọc các bài viết về ExtractThinker trên trang Medium của tác giả.
- **Bộ kiểm thử (Test Suite)**: Khám phá bộ kiểm thử trong thư mục tests/ để biết thêm các ví dụ sử dụng nâng cao và các trường hợp kiểm thử.

## 🧩 Tích hợp với các nhà cung cấp LLM

ExtractThinker hỗ trợ tích hợp với nhiều nhà cung cấp LLM:

- **OpenAI**: Sử dụng các mô hình như gpt-3.5-turbo, gpt-4, v.v.
- **Anthropic**: Tích hợp với các mô hình Claude.
- **Cohere**: Sử dụng các mô hình ngôn ngữ của Cohere.
- **Azure OpenAI**: Kết nối với các dịch vụ OpenAI của Azure.
- **Mô hình cục bộ**: Các mô hình tương thích với Ollama.

## ⚙️ Cách thức hoạt động

ExtractThinker sử dụng kiến trúc mô đun lấy cảm hứng từ hệ sinh thái LangChain:

- **Document Loaders (Trình tải tài liệu)**: Chịu trách nhiệm tải và tiền xử lý tài liệu từ nhiều nguồn và định dạng khác nhau.
- **Extractors (Trình trích xuất)**: Điều phối sự tương tác giữa các trình tải tài liệu và LLM để trích xuất dữ liệu có cấu trúc.
- **Splitters (Trình chia nhỏ)**: Triển khai các chiến lược để chia tài liệu thành các phần có thể quản lý được để xử lý.
- **Contracts**: Xác định cấu trúc mong đợi của dữ liệu được trích xuất bằng cách sử dụng các mô hình Pydantic.
- **Classifications (Phân loại)**: Phân loại tài liệu hoặc các phần của tài liệu để áp dụng các contract trích xuất phù hợp.
- **Processes (Quy trình)**: Quản lý quy trình làm việc gồm tải, phân loại, chia nhỏ và trích xuất dữ liệu từ tài liệu.

![image](https://github.com/user-attachments/assets/b12ba937-20a8-47da-a778-c126bc1748b3)

## 📝 Tại sao nên sử dụng ExtractThinker?

Trong khi các framework chung như LangChain cung cấp một loạt các chức năng, ExtractThinker được chuyên biệt hóa cho Xử lý Tài liệu Thông minh (IDP). Nó đơn giản hóa các sự phức tạp liên quan đến IDP bằng cách cung cấp:

- **Các thành phần chuyên biệt**: Các công cụ được thiết kế riêng cho việc tải, chia nhỏ và trích xuất tài liệu.
- **Độ chính xác cao với LLM**: Tận dụng sức mạnh của LLM để cải thiện độ chính xác của việc trích xuất và phân loại dữ liệu.
- **Dễ sử dụng**: API trực quan và tương tác kiểu ORM giúp giảm bớt khó khăn khi học.
- **Hỗ trợ từ cộng đồng**: Phát triển tích cực và được hỗ trợ bởi cộng đồng.

## 🤝 Đóng góp

Chúng tôi hoan nghênh sự đóng góp từ cộng đồng! Để đóng góp:

1. Fork kho lưu trữ (repository)
2. Tạo một nhánh (branch) mới cho tính năng hoặc bản sửa lỗi của bạn
3. Viết các bài kiểm thử (tests) cho các thay đổi của bạn
4. Chạy các bài kiểm thử để đảm bảo mọi thứ hoạt động chính xác
5. Gửi một yêu cầu kéo (pull request - PR) với mô tả về các thay đổi của bạn

## 🌟 Cộng đồng và Hỗ trợ

Cập nhật thông tin và kết nối với cộng đồng:
- [Scaling Document Extraction with o1, GPT-4o & Mini](https://medium.com/towards-artificial-intelligence/scaling-document-extraction-with-o1-gpt4o-and-mini-extractthinker-8f3340b4e69c)
- [Claude 3.5 — The King of Document Intelligence](https://medium.com/gitconnected/claude-3-5-the-king-of-document-intelligence-f57bea1d209d?sk=124c5abb30c0e7f04313c5e20e79c2d1)
- [Classification Tree for LLMs](https://medium.com/gitconnected/classification-tree-for-llms-32b69015c5e0?sk=8a258cf74fe3483e68ab164e6b3aaf4c)
- [Advanced Document Classification with LLMs](https://medium.com/gitconnected/advanced-document-classification-with-llms-8801eaee3c58?sk=f5a22ee72022eb70e112e3e2d1608e79)
- [Phi-3 and Azure: PDF Data Extraction | ExtractThinker](https://medium.com/towards-artificial-intelligence/phi-3-and-azure-pdf-data-extraction-extractthinker-cb490a095adb?sk=7be7e625b8f9932768442f87dd0ebcec)
- [ExtractThinker: Document Intelligence for LLMs](https://medium.com/towards-artificial-intelligence/extractthinker-ai-document-intelligence-with-llms-72cbce1890ef)

## 📄 Giấy phép

Dự án này được cấp phép theo Giấy phép Apache 2.0. Xem tệp LICENSE để biết thêm chi tiết.

## Liên hệ

Đối với bất kỳ câu hỏi hoặc vấn đề nào, vui lòng mở một issue trên kho lưu trữ GitHub hoặc liên hệ qua email.
