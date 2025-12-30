import json
import os
from contracts.finance.invoice import VietnamInvoice
from contracts.finance.bank_transfer import VietnamBankTransfer
from contracts.finance.contract import VietnamContract
from contracts.identity.cccd import VietnamCCCD
from contracts.identity.passport import VietnamPassport
from contracts.identity.birth_cert import VietnamBirthCert
from contracts.vehicle.vehicle_reg import VietnamVehicleReg
from contracts.vehicle.driver_license import VietnamDriverLicense
from contracts.vehicle.inspection import VietnamInspection

def generate_schema(model, name):
    schema = model.model_json_schema()
    # Simplify schema to just properties for easy reading
    props = schema.get('properties', {})
    template = {k: f"<{v.get('description', '')}>" for k, v in props.items()}
    return template

MODELS = {
    'finance/invoice': VietnamInvoice,
    'finance/bank_transfer': VietnamBankTransfer,
    'finance/contract': VietnamContract,
    'identity/cccd': VietnamCCCD,
    'identity/passport': VietnamPassport,
    'identity/birth_cert': VietnamBirthCert,
    'vehicle/vehicle_reg': VietnamVehicleReg,
    'vehicle/driver_license': VietnamDriverLicense,
    'vehicle/inspection': VietnamInspection
}

def main():
    base_dir = "dataset"
    print("Generating schemas for dataset...")
    
    for path, model in MODELS.items():
        template = generate_schema(model, path)
        gt_dir = os.path.join(base_dir, path, "ground_truth")
        
        # Save a _schema.json file in each ground_truth folder
        schema_path = os.path.join(gt_dir, "_schema.json")
        with open(schema_path, "w", encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"✅ Generated schema for {path}")

if __name__ == "__main__":
    main()
