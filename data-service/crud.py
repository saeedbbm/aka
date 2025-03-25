import models
from datetime import datetime

def save_record(db, record):
    # 1. Get or create patient
    patient = db.query(models.Patient).filter_by(id=record.patient_id).first()
    if not patient:
        patient = models.Patient(id=record.patient_id, name=record.name)
        db.add(patient)
        db.flush()  # flush to generate any defaults if needed

    # 2. Create claim
    claim = models.Claim(patient_id=patient.id, date=datetime.utcnow())
    db.add(claim)
    db.flush()

    # 3. Create diagnosis
    diagnosis = models.Diagnosis(claim_id=claim.id, icd_code=record.icd10_code, description=record.diagnosis)
    db.add(diagnosis)

    # 4. Create medication
    medication = models.Medication(claim_id=claim.id, name=record.medication, dosage=record.dosage)
    db.add(medication)

    # 5. Commit all changes
    db.commit()
    return claim.id
