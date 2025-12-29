from extract_thinker import Contract
from pydantic import Field, BaseModel
from typing import Optional, List

# Class con cho từng dòng hàng hóa
class InvoiceItem(BaseModel):
    ten_hang: Optional[str] = Field(None, description="Tên hàng hóa, dịch vụ")
    so_luong: Optional[str] = Field(None, description="Số lượng")
    don_gia: Optional[str] = Field(None, description="Đơn giá")
    thanh_tien: Optional[str] = Field(None, description="Thành tiền")

class VietnamInvoice(Contract):
    
    # Thông tin chung quan trọng
    so_hoa_don: Optional[str] = Field(None, description="Số hóa đơn")
    ngay_hoa_don: Optional[str] = Field(None, description="Ngày lập hóa đơn")
    
    # Bên bán
    ten_nguoi_ban: Optional[str] = Field(None, description="Tên đơn vị bán hàng")
    mst_nguoi_ban: Optional[str] = Field(None, description="Mã số thuế người bán")
    
    # Chi tiết hàng hóa (Quan trọng)
    danh_sach_mat_hang: Optional[List[InvoiceItem]] = Field(None, description="Danh sách chi tiết hàng hóa, dịch vụ")
    
    # Tổng cộng
    tong_tien_thanh_toan: Optional[str] = Field(None, description="Tổng tiền thanh toán")
