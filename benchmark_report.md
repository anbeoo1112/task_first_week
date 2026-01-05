# Báo cáo Benchmark: Prompt Engineering vs Tool/Function Calling

## Tóm tắt
Chúng tôi đã so sánh hai phương pháp trích xuất dữ liệu có cấu trúc từ tài liệu sử dụng **Gemini 2.0 Flash**:
1.  **Prompt Mode** (`is_dynamic=True`): Schema được chuyển đổi thành văn bản prompt + JSON parsing.
2.  **Tool Mode** (`is_dynamic=False`): Schema được truyền dưới dạng Function Definition (Native Tool Calling).

**Kết luận chính:** **Tool Mode nhanh hơn ~2.1 lần và đáng tin cậy hơn** so với Prompt Mode.

## Kết quả chi tiết

| Chỉ số | Prompt Mode | Tool Mode | Khác biệt |
| :--- | :--- | :--- | :--- |
| **Độ trễ trung bình** | **2,890 ms** (~2.9 giây) | **1,361 ms** (~1.4 giây) | **Tool nhanh hơn ~53%** |
| **Tỷ lệ thành công** | 17/20 (85%) | **20/20 (100%)** | **Tool ổn định hơn** |

### Quan sát
- **Độ tin cậy (Lỗi ở `Prompt Mode`)**: Prompt Mode thất bại trong 3 trường hợp do **Lỗi Validation Pydantic**. Model trả về một danh sách (ví dụ: `["COV", "LMV"]`) cho trường `hang` (Hạng xe), trong khi schema yêu cầu một chuỗi đơn. Tool Mode đã xử lý chính xác bằng cách gộp thành một chuỗi (ví dụ: `"COV, LMV"`), cho thấy sự tuân thủ schema tốt hơn.
- **Sự ổn định**: Tool Mode có độ biến động thời gian thấp hơn nhiều (~1.2s - 1.5s), trong khi Prompt Mode dao động đáng kể (~1.8s - 3.6s).

## Tại sao Tool Mode tốt hơn?
1.  **Tốc độ**: Native function calling được tối ưu hóa ở phía model, bỏ qua việc phải sinh ra các token JSON dài dòng rồi mới parse lại.
2.  **Sự mạnh mẽ (Robustness)**: Model bị "ép buộc" phải tuân theo function signature, giảm thiểu các format ảo giác hoặc sai kiểu dữ liệu (như List vs String).
3.  **Token Usage**: Cách định nghĩa Tool thường tiết kiệm token hơn so với các system prompt dài dòng mô tả JSON schema.

## Khuyến nghị
**Sử dụng Tool/Function Calling (`is_dynamic=False`)** làm chiến lược mặc định cho tất cả các tác vụ trích xuất.
