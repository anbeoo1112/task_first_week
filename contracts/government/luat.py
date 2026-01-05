from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class Luat(Contract):
    """Văn bản Luật của Quốc hội"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu luật")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu của luật")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
