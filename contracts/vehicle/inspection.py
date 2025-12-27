from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamInspection(Contract):
    bien_so_xe: Optional[str] = Field(None, description="Biển số xe")
    ngay_kiem_dinh: Optional[str] = Field(None, description="Ngày kiểm định")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")
    so_tem: Optional[str] = Field(None, description="Số tem đăng kiểm")
    trung_tam_dk: Optional[str] = Field(None, description="Trung tâm đăng kiểm")
