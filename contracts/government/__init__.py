from .nghi_quyet import NghiQuyetChinhPhu, NghiQuyetPhienHopChinhPhu
from .van_ban import (
    VanBanChiDaoDieuHanh, 
    VanBanHopNhat, 
    Luat,
    PhapLenh,
    Lenh,
    NghiDinh,
    ThongTu,
    SacLuat,
    SacLenh
)

GOVERNMENT_DOCS = {
    "NghiQuyetChinhPhu": ("Nghị quyết Chính phủ", NghiQuyetChinhPhu),
    "NghiQuyetPhienHopChinhPhu": ("Nghị quyết phiên họp Chính phủ", NghiQuyetPhienHopChinhPhu),
    "VanBanChiDaoDieuHanh": ("Văn bản chỉ đạo điều hành", VanBanChiDaoDieuHanh),
    "VanBanHopNhat": ("Văn bản hợp nhất", VanBanHopNhat),
    "Luat": ("Luật - Văn bản Luật", Luat),
    "PhapLenh": ("Pháp lệnh", PhapLenh),
    "Lenh": ("Lệnh - Chủ tịch nước", Lenh),
    "NghiDinh": ("Nghị định - Chính phủ", NghiDinh),
    "ThongTu": ("Thông tư", ThongTu),
    "SacLuat": ("Sắc luật", SacLuat),
    "SacLenh": ("Sắc lệnh", SacLenh)
}

__all__ = [
    "NghiQuyetChinhPhu",
    "NghiQuyetPhienHopChinhPhu",
    "VanBanChiDaoDieuHanh",
    "VanBanHopNhat",
    "Luat",
    "PhapLenh",
    "Lenh",
    "NghiDinh",
    "ThongTu",
    "SacLuat",
    "SacLenh",
    "GOVERNMENT_DOCS"
]
