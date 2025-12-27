from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamVehicleReg(Contract):
    bien_so_xe: Optional[str] = Field(None, description="Biển số xe")
    nhan_hieu: Optional[str] = Field(None, description="Nhãn hiệu")
    mau_xe: Optional[str] = Field(None, description="Màu xe")
    so_khung: Optional[str] = Field(None, description="Số khung")
    so_may: Optional[str] = Field(None, description="Số máy")
    ten_chu_xe: Optional[str] = Field(None, description="Tên chủ xe")
    so: Optional[str] = Field(None, description="Số đăng ký")
