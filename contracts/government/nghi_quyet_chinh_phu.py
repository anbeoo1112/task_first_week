from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class NghiQuyetChinhPhu(Contract):
    """Văn bản Nghị quyết"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu văn bản")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Trích yếu nội dung")
    co_quan_ban_hanh: Optional[str] = Field(None, description="Cơ quan ban hành")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
