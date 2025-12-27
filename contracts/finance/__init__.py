from .contract import VietnamContract
from .bank_transfer import VietnamBankTransfer

FINANCE_DOCS = {
    "hop_dong": ("Hợp đồng", VietnamContract),
    "chuyen_khoan": ("Bill chuyển khoản", VietnamBankTransfer),
}
