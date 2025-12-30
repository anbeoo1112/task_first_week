from extract_thinker import Contract
from pydantic import Field, BaseModel
from typing import Optional, List

class InvoiceItem(BaseModel):
    """Chi tiết một mặt hàng trong hóa đơn"""
    ten_hang: str = Field(
        default="UNKNOWN", 
        description="Tên sản phẩm. VD: ENGINE OIL, STARTER TALI. BẮT BUỘC phải điền."
    )
    ma_hang: str = Field(
        default="UNKNOWN", 
        description="Mã hàng/SKU. VD: 1072, 70549. BẮT BUỘC phải điền."
    )
    so_luong: Optional[float] = Field(None, description="Số lượng")
    don_gia: Optional[float] = Field(None, description="Đơn giá")
    thanh_tien: Optional[float] = Field(None, description="Thành tiền")



class Invoice(Contract):
    """Hóa đơn bán lẻ Malaysia"""
    ten_cua_hang: Optional[str] = Field(None, description="Tên cửa hàng ở đầu hóa đơn")
    dia_chi: Optional[str] = Field(None, description="Địa chỉ cửa hàng")
    so_hoa_don: Optional[str] = Field(None, description="Số hóa đơn (Doc No, Document No)")
    ngay_hoa_don: Optional[str] = Field(None, description="Ngày lập hóa đơn")
    danh_sach_mat_hang: Optional[List[InvoiceItem]] = Field(
        None, 
        description="""Danh sách sản phẩm. Mỗi sản phẩm CẦN có ten_hang và ma_hang.
        Trong OCR: mã hàng là số ngắn (VD: 1072, 70549), tên hàng là text mô tả (VD: ENGINE OIL, STARTER TALI).
        KHÔNG để ten_hang = null."""
    )
    tong_tien: Optional[float] = Field(None, description="Total Sales")
    tong_thanh_toan: Optional[float] = Field(None, description="Rounded Total / Tổng cuối cùng")


INVOICE_EXTRA_CONTENT = """
Đây là Hóa đơn/Receipt bán lẻ Malaysia. Có nhiều format khác nhau.

=== FORMAT 1: Mã hàng + Tên hàng CÙNG DÒNG ===
Ví dụ OCR:
```
9556939040118 KF MODELLING CLAY KIDDY FISH
1 PC
9.000 0.00
9.00
```
Kết quả:
- ma_hang: "9556939040118"
- ten_hang: "KF MODELLING CLAY KIDDY FISH"  
- so_luong: 1
- don_gia: 9.00
- thanh_tien: 9.00

=== FORMAT 2: Mã hàng TRƯỚC, Tên hàng SAU (dòng riêng) ===
Ví dụ OCR:
```
1072
1
80.00 80.00
80.00
REPAIR ENGINE POWER SPRAYER (1UNIT)
```
Kết quả:
- ma_hang: "1072"
- ten_hang: "REPAIR ENGINE POWER SPRAYER (1UNIT)"
- so_luong: 1
- don_gia: 80.00
- thanh_tien: 80.00

=== FORMAT 3: Nhiều hàng liên tiếp ===
```
70549
1
160.00 160.00
160.00
GIANT 606 OVERFLOW ASSY
1071
1
17.00 17.00
17.00
ENGINE OIL
```
Mỗi nhóm = 1 InvoiceItem:
- Item 1: ma_hang="70549", ten_hang="GIANT 606 OVERFLOW ASSY", so_luong=1, don_gia=160, thanh_tien=160
- Item 2: ma_hang="1071", ten_hang="ENGINE OIL", so_luong=1, don_gia=17, thanh_tien=17

=== CÁCH NHẬN BIẾT ===
- MÃ HÀNG: Chuỗi số hoặc chữ-số ngắn (4-13 ký tự). VD: 1072, 70549, 9556939040118
- TÊN HÀNG: Text dài, chứa chữ cái, mô tả sản phẩm. VD: "ENGINE OIL", "STARTER TALI"
- SỐ LƯỢNG: Số nhỏ (1, 2, 5...)
- GIÁ/TIỀN: Số có dấu chấm thập phân (80.00, 17.00...)

QUAN TRỌNG: PHẢI trích xuất ten_hang và ma_hang. KHÔNG được để null!
"""


