from extract_thinker import Contract
from pydantic import Field
from typing import Optional

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
