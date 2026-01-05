from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class Lenh(Contract):
    """Lệnh của Chủ tịch nước"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu lệnh")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
