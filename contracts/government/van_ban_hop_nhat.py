from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VanBanHopNhat(Contract):
    """Văn bản chính phủ"""
    so_kieu: Optional[str] = Field(None, description="Số và ký hiệu")
    ngay: Optional[str] = Field(None, description="Ngày tháng năm")
    tieu_de: Optional[str] = Field(None, description="Tiêu đề văn bản")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
