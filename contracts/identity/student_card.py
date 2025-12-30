from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamStudentCard(Contract):
    """Thẻ sinh viên"""
    ma_sv: Optional[str] = Field(None, description="Mã số sinh viên")
    ho_ten: Optional[str] = Field(None, description="Họ và tên")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    lop: Optional[str] = Field(None, description="Lớp")
    khoa: Optional[str] = Field(None, description="Khoa")
    nganh: Optional[str] = Field(None, description="Ngành")
    khoa_hoc: Optional[str] = Field(None, description="Khóa học")
    truong: Optional[str] = Field(None, description="Tên trường")


STUDENT_CARD_EXTRA_CONTENT = """
Đây là Thẻ sinh viên.
- Mã SV: dãy số hoặc chữ-số
- Họ tên: viết đầy đủ
- Lớp: mã lớp
- Khoa: tên khoa/viện
- Ngành: tên ngành học
- Khóa: năm nhập học (K65, D19...)
- Trường: tên trường đại học
"""
