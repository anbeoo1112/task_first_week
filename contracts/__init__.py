from contracts.identity import IDENTITY_DOCS, VietnamCCCD, VietnamPassport, VietnamStudentCard
from contracts.identity import CCCD_EXTRA_CONTENT, PASSPORT_EXTRA_CONTENT, STUDENT_CARD_EXTRA_CONTENT
from contracts.vehicle import VEHICLE_DOCS, VietnamDriverLicense, DRIVER_LICENSE_EXTRA_CONTENT
from contracts.finance import FINANCE_DOCS, Invoice, INVOICE_EXTRA_CONTENT

DOCUMENT_CATEGORIES = {
    "identity": IDENTITY_DOCS,
    "vehicle": VEHICLE_DOCS,
    "finance": FINANCE_DOCS,
}

ALL_CONTRACTS = {
    **IDENTITY_DOCS,
    **VEHICLE_DOCS,
    **FINANCE_DOCS,
}

# Map contract -> extra_content
EXTRA_CONTENTS = {
    VietnamCCCD: CCCD_EXTRA_CONTENT,
    VietnamPassport: PASSPORT_EXTRA_CONTENT,
    VietnamStudentCard: STUDENT_CARD_EXTRA_CONTENT,
    VietnamDriverLicense: DRIVER_LICENSE_EXTRA_CONTENT,
    Invoice: INVOICE_EXTRA_CONTENT,
}
