from .cccd import VietnamCCCD, CCCD_EXTRA_CONTENT
from .passport import VietnamPassport, PASSPORT_EXTRA_CONTENT
from .student_card import VietnamStudentCard, STUDENT_CARD_EXTRA_CONTENT

IDENTITY_DOCS = {
    "cccd": ("Căn cước công dân", VietnamCCCD),
    "passport": ("Hộ chiếu", VietnamPassport),
    "student_card": ("Thẻ sinh viên", VietnamStudentCard),
}
