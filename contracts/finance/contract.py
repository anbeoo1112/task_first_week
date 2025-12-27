from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamContract(Contract):
    so_hop_dong: Optional[str] = Field(None, description="Số hợp đồng")
    ngay_ky: Optional[str] = Field(None, description="Ngày ký")
    ben_a: Optional[str] = Field(None, description="Tên bên A")
    ben_b: Optional[str] = Field(None, description="Tên bên B")
    noi_dung_chinh: Optional[str] = Field(None, description="Nội dung chính của hợp đồng")
    gia_tri_hop_dong: Optional[str] = Field(None, description="Giá trị hợp đồng")
    thoi_han: Optional[str] = Field(None, description="Thời hạn hợp đồng")
