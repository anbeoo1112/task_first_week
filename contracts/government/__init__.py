from .nghi_quyet_chinh_phu import NghiQuyetChinhPhu
from .nghi_quyet_phien_hop import NghiQuyetPhienHopChinhPhu
from .van_ban_chi_dao import VanBanChiDaoDieuHanh
from .van_ban_hop_nhat import VanBanHopNhat
from .luat import Luat
from .phap_lenh import PhapLenh
from .lenh import Lenh
from .nghi_dinh import NghiDinh
from .thong_tu import ThongTu

# Chia thành các nhóm nhỏ để cây phân loại cân bằng hơn

# Nhóm 1: Văn bản quy phạm pháp luật (do Quốc hội, Chính phủ ban hành)
GOV_LEGAL_DOCS = {
    "Luat": ("Luật - Văn bản Luật", Luat),
    "PhapLenh": ("Pháp lệnh", PhapLenh),
    "NghiDinh": ("Nghị định - Chính phủ", NghiDinh),
    "ThongTu": ("Thông tư", ThongTu),
}

# Nhóm 2: Văn bản hành chính (nghị quyết, lệnh, chỉ đạo điều hành)
GOV_ADMIN_DOCS = {
    "NghiQuyetChinhPhu": ("Nghị quyết Chính phủ", NghiQuyetChinhPhu),
    "NghiQuyetPhienHopChinhPhu": ("Nghị quyết phiên họp Chính phủ", NghiQuyetPhienHopChinhPhu),
    "Lenh": ("Lệnh - Chủ tịch nước", Lenh),
    "VanBanChiDaoDieuHanh": ("Văn bản chỉ đạo điều hành", VanBanChiDaoDieuHanh),
    "VanBanHopNhat": ("Văn bản hợp nhất", VanBanHopNhat),
}

# Backward compatibility - giữ GOVERNMENT_DOCS để code cũ không bị hỏng
GOVERNMENT_DOCS = {
    **GOV_LEGAL_DOCS,
    **GOV_ADMIN_DOCS,
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
    "GOV_LEGAL_DOCS",
    "GOV_ADMIN_DOCS", 
    "GOVERNMENT_DOCS"
]
