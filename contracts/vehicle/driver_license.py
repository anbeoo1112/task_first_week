from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamDriverLicense(Contract):
    """Giấy phép lái xe"""
    so_gplx: Optional[str] = Field(None, description="Số GPLX")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    hang: Optional[str] = Field(None, description="Hạng (A1, B2, C...)")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Có giá trị đến")
    noi_cap: Optional[str] = Field(None, description="Nơi cấp")


DRIVER_LICENSE_EXTRA_CONTENT = """
Đây là Giấy phép lái xe Việt Nam.
- Số GPLX: 12 chữ số
- Hạng: A1, A2, B1, B2, C, D, E, F
- Nơi cấp: Sở GTVT hoặc Cục CSGT
"""
