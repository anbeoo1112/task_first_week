from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamCCCD(Contract):
    """Căn cước công dân Việt Nam"""
    so_cccd: Optional[str] = Field(None, description="Số CCCD 12 chữ số")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    gioi_tinh: Optional[str] = Field(None, description="Giới tính")
    quoc_tich: Optional[str] = Field(None, description="Quốc tịch")
    que_quan: Optional[str] = Field(None, description="Quê quán")
    noi_thuong_tru: Optional[str] = Field(None, description="Nơi thường trú")
    ngay_het_han: Optional[str] = Field(None, description="Ngày hết hạn")


CCCD_EXTRA_CONTENT = """
Đây là Căn cước công dân Việt Nam (CCCD).
- Số CCCD: dãy 12 số ở góc trên phải
- Họ tên: viết IN HOA có dấu
- Ngày sinh: DD/MM/YYYY
- Quê quán và Nơi thường trú: địa chỉ đầy đủ
"""
