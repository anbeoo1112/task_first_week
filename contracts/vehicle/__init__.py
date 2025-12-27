from .driver_license import VietnamDriverLicense
from .vehicle_reg import VietnamVehicleReg
from .inspection import VietnamInspection

VEHICLE_DOCS = {
    "bang_lai": ("Bằng lái xe", VietnamDriverLicense),
    "dang_ky_xe": ("Đăng ký xe", VietnamVehicleReg),
    "dang_kiem": ("Đăng kiểm xe", VietnamInspection),
}
