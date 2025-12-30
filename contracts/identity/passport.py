from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamPassport(Contract):
    """Hộ chiếu"""
    loai: Optional[str] = Field(None, description="Loại (P, PD...)")
    ma_so: Optional[str] = Field(None, description="Mã số quốc gia")
    so_ho_chieu: Optional[str] = Field(None, description="Số hộ chiếu")
    ho: Optional[str] = Field(None, description="Họ (Surname)")
    chu_dem_va_ten: Optional[str] = Field(None, description="Tên (Given names)")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính (M/F)")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")


PASSPORT_EXTRA_CONTENT = """
Đây là Hộ chiếu (Passport).
- Type/Loại: P = Passport thường
- Số hộ chiếu: chuỗi chữ số như B1234567
- Surname/Họ: viết IN HOA không dấu  
- Given names/Tên: viết IN HOA không dấu
- Sex: M = Nam, F = Nữ
- Bỏ qua dòng MRZ (2 dòng mã ở cuối)
"""
