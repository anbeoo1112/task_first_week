from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamDriverLicense(Contract):
    so_bang_lai: Optional[str] = Field(None, description="Số bằng lái")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    hang_bang_lai: Optional[str] = Field(None, description="Hạng bằng lái (A1, A2, B1, B2, C...)")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")
