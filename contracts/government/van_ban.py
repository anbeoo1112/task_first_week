from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VanBanChiDaoDieuHanh(Contract):
    """Văn bản chính phủ"""
    so_kieu: Optional[str] = Field(None, description="Số và ký hiệu")
    ngay: Optional[str] = Field(None, description="Ngày tháng năm")
    tieu_de: Optional[str] = Field(None, description="Tiêu đề văn bản")
    nguoi_ky: Optional[str] = Field(None, description="Người ký")

class VanBanHopNhat(Contract):
    """Văn bản chính phủ"""
    so_kieu: Optional[str] = Field(None, description="Số và ký hiệu")
    ngay: Optional[str] = Field(None, description="Ngày tháng năm")
    tieu_de: Optional[str] = Field(None, description="Tiêu đề văn bản")
    nguoi_ky: Optional[str] = Field(None, description="Người ký")

class Luat(Contract):
    """Văn bản Luật của Quốc hội"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu luật")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu của luật")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class PhapLenh(Contract):
    """Văn bản Pháp lệnh của UBTVQH"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu pháp lệnh")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class Lenh(Contract):
    """Lệnh của Chủ tịch nước"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu lệnh")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class NghiDinh(Contract):
    """Nghị định của Chính phủ"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu nghị định")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class ThongTu(Contract):
    """Thông tư của Bộ/Cơ quan ngang bộ"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu thông tư")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class SacLuat(Contract):
    """Sắc luật (Văn bản có giá trị như luật)"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu sắc luật")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")

class SacLenh(Contract):
    """Sắc lệnh (Văn bản của Chủ tịch nước/Chính phủ cũ)"""
    so_hieu: Optional[str] = Field(None, description="Số hiệu sắc lệnh")
    ngay_ban_hanh: Optional[str] = Field(None, description="Ngày ban hành")
    trich_yeu: Optional[str] = Field(None, description="Tên gọi/Trích yếu")
    nguoi_ky: Optional[str] = Field(None, description="Người ký văn bản")
