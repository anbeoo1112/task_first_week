from extract_thinker import Contract
from pydantic import Field
from typing import Optional


class VietnamCCCD(Contract):
    so_cccd: Optional[str] = Field(None, description="Số CCCD 12 chữ số")
    ho_ten: Optional[str] = Field(None, description="Họ và tên đầy đủ")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh (dd/mm/yyyy)")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    que_quan: Optional[str] = Field(None, description="Quê quán")
    noi_thuong_tru: Optional[str] = Field(None, description="Nơi thường trú")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")


class VietnamPassport(Contract):
    loai: Optional[str] = Field(None, description="Loại hộ chiếu (P, PD, PS...)")
    ma_so: Optional[str] = Field(None, description="Mã số")
    so_ho_chieu: Optional[str] = Field(None, description="Số hộ chiếu")
    ho: Optional[str] = Field(None, description="Họ (Surname)")
    chu_dem_va_ten: Optional[str] = Field(None, description="Chữ đệm và tên (Given names)")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính")
    so_cccd: Optional[str] = Field(None, description="Số CCCD liên kết")
    ngay_cap: Optional[str] = Field(None, description="Ngày cấp")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")


class VietnamBirthCert(Contract):
    so_giay: Optional[str] = Field(None, description="Số giấy khai sinh")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính")
    dan_toc: Optional[str] = Field(None, description="Dân tộc")
    noi_sinh: Optional[str] = Field(None, description="Nơi sinh")
    que_quan: Optional[str] = Field(None, description="Quê quán")
    ho_ten_cha: Optional[str] = Field(None, description="Họ tên cha")
    ho_ten_me: Optional[str] = Field(None, description="Họ tên mẹ")


# Document type mapping
IDENTITY_DOCS = {
    "cccd": ("Căn cước công dân", VietnamCCCD),
    "ho_chieu": ("Hộ chiếu", VietnamPassport),
    "giay_khai_sinh": ("Giấy khai sinh", VietnamBirthCert),
}