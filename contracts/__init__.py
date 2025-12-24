"""
Contracts package - Vietnamese document schemas
Export all document types for easy import
"""
# Identity documents
from contracts.identity import (
    VietnamCCCD,
    VietnamPassport, 
    VietnamBirthCert,
    IDENTITY_DOCS
)

# Vehicle documents
from contracts.vehicle import (
    VietnamDriverLicense,
    VietnamVehicleReg,
    VietnamInspection,
    VEHICLE_DOCS
)

# Finance documents
from contracts.finance import (
    VietnamContract,
    VietnamBankTransfer,
    FINANCE_DOCS
)

# All document categories
DOCUMENT_CATEGORIES = {
    "identity": ("Giấy tờ tùy thân", IDENTITY_DOCS),
    "vehicle": ("Giấy tờ phương tiện", VEHICLE_DOCS),
    "finance": ("Giấy tờ tài chính", FINANCE_DOCS),
}

# All contracts list (for Classification)
ALL_CONTRACTS = [
    # Identity
    VietnamCCCD,
    VietnamPassport,
    VietnamBirthCert,
    # Vehicle
    VietnamDriverLicense,
    VietnamVehicleReg,
    VietnamInspection,
    # Finance
    VietnamContract,
    VietnamBankTransfer,
]
