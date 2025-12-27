from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamPassport(Contract):
    loai: Optional[str] = Field(None, description="Loại hộ chiếu (P, PD, PS...)")
    ma_so: Optional[str] = Field(None, description="Mã số")
    so_ho_chieu: Optional[str] = Field(None, description="Số hộ chiếu")
    ho: Optional[str] = Field(None, description="Họ (Surname)")
    chu_dem_va_ten: Optional[str] = Field(None, description="Chữ đệm và tên (Given names)")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính")
    so_cccd: Optional[str] = Field(None, description="Số CCCD liên kết")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")
