from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class ThongTu(Contract):
    """Thông tư của Bộ/Cơ quan ngang bộ"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu thông tư")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
