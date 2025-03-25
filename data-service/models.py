from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True)  # assuming patient_id is provided as text/UUID
    name = Column(String(100), default="Unknown")
    claims = relationship("Claim", back_populates="patient")

class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="claims")
    diagnoses = relationship("Diagnosis", back_populates="claim")
    medications = relationship("Medication", back_populates="claim")

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    icd_code = Column(String(10), index=True)
    description = Column(String(255))
    claim = relationship("Claim", back_populates="diagnoses")

class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    name = Column(String(100))
    dosage = Column(String(50))
    claim = relationship("Claim", back_populates="medications")
