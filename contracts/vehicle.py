"""
Vehicle Documents - Giấy tờ phương tiện
Sử dụng extract_thinker Contract cho tương thích với ExtractThinker library
"""
from extract_thinker import Contract
from pydantic import Field
from typing import Optional


class VietnamDriverLicense(Contract):
    so_bang_lai: Optional[str] = Field(None, description="Số bằng lái")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    hang_bang_lai: Optional[str] = Field(None, description="Hạng bằng lái (A1, A2, B1, B2, C...)")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")


class VietnamVehicleReg(Contract):
    bien_so_xe: Optional[str] = Field(None, description="Biển số xe")
    nhan_hieu: Optional[str] = Field(None, description="Nhãn hiệu")
    mau_xe: Optional[str] = Field(None, description="Màu xe")
    so_khung: Optional[str] = Field(None, description="Số khung")
    so_may: Optional[str] = Field(None, description="Số máy")
    ten_chu_xe: Optional[str] = Field(None, description="Tên chủ xe")
    so: Optional[str] = Field(None, description="Số đăng ký")
    


class VietnamInspection(Contract):
    bien_so_xe: Optional[str] = Field(None, description="Biển số xe")
    ngay_kiem_dinh: Optional[str] = Field(None, description="Ngày kiểm định")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")
    so_tem: Optional[str] = Field(None, description="Số tem đăng kiểm")
    trung_tam_dk: Optional[str] = Field(None, description="Trung tâm đăng kiểm")


VEHICLE_DOCS = {
    "bang_lai": ("Bằng lái xe", VietnamDriverLicense),
    "dang_ky_xe": ("Đăng ký xe", VietnamVehicleReg),
    "dang_kiem": ("Đăng kiểm xe", VietnamInspection),
}
