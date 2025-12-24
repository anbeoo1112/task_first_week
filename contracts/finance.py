from extract_thinker import Contract
from pydantic import Field
from typing import Optional

class VietnamContract(Contract):
    so_hop_dong: Optional[str] = Field(None, description="Số hợp đồng")
    ngay_ky: Optional[str] = Field(None, description="Ngày ký")
    ben_a: Optional[str] = Field(None, description="Tên bên A")
    ben_b: Optional[str] = Field(None, description="Tên bên B")
    noi_dung_chinh: Optional[str] = Field(None, description="Nội dung chính của hợp đồng")
    gia_tri_hop_dong: Optional[str] = Field(None, description="Giá trị hợp đồng")
    thoi_han: Optional[str] = Field(None, description="Thời hạn hợp đồng")


class VietnamBankTransfer(Contract):
    """Bill chuyển khoản ngân hàng"""
    # Thông tin giao dịch
    trang_thai: Optional[str] = Field(None, description="Trạng thái giao dịch (thành công/thất bại)")
    so_tien: Optional[str] = Field(None, description="Số tiền giao dịch")
    
    # Từ tài khoản (người chuyển)
    ten_nguoi_chuyen: Optional[str] = Field(None, description="Tên người chuyển tiền")
    so_tai_khoan_nguoi_chuyen: Optional[str] = Field(None, description="Số tài khoản người chuyển")
    
    # Tới tài khoản (người nhận)
    ten_nguoi_nhan: Optional[str] = Field(None, description="Tên người nhận tiền")
    so_tai_khoan_nguoi_nhan: Optional[str] = Field(None, description="Số tài khoản người nhận")
    ten_ngan_hang_nhan: Optional[str] = Field(None, description="Tên ngân hàng người nhận")
    
    # Chi tiết giao dịch
    thoi_gian: Optional[str] = Field(None, description="Thời gian thực hiện giao dịch")
    ma_giao_dich: Optional[str] = Field(None, description="Mã giao dịch")
    noi_dung_chuyen_tien: Optional[str] = Field(None, description="Nội dung chuyển tiền")
    phuong_thuc: Optional[str] = Field(None, description="Phương thức/cách thức chuyển tiền (Napas, SWIFT, ...)")


FINANCE_DOCS = {
    "hop_dong": ("Hợp đồng", VietnamContract),
    "chuyen_khoan": ("Bill chuyển khoản", VietnamBankTransfer),
}

