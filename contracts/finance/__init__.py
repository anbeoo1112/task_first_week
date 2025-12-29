from .contract import VietnamContract
from .bank_transfer import VietnamBankTransfer
from .invoice import VietnamInvoice

FINANCE_DOCS = {
    "hop_dong": ("Hợp đồng", VietnamContract),
    "chuyen_khoan": ("Bill chuyển khoản", VietnamBankTransfer),
    "hoa_don": ("Hóa đơn bán hàng", VietnamInvoice),
}
