from .cccd import VietnamCCCD
from .passport import VietnamPassport
from .birth_cert import VietnamBirthCert

# Document type mapping
IDENTITY_DOCS = {
    "cccd": ("Căn cước công dân", VietnamCCCD),
    "ho_chieu": ("Hộ chiếu", VietnamPassport),
    "giay_khai_sinh": ("Giấy khai sinh", VietnamBirthCert),
}
