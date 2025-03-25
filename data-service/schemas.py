from pydantic import BaseModel

class RecordCreate(BaseModel):
    patient_id: str
    name: str = "Unknown"  # optional: if not provided, default to "Unknown"
    medication: str
    dosage: str
    diagnosis: str
    icd10_code: str
