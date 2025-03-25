from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Header

DATABASE_URL = "postgresql://postgres:postgres@db/main"

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_session(tenant_id: str = Header(..., alias="X-Tenant-ID")):
    db = SessionLocal()
    try:
        db.execute(text(f"SET search_path TO {tenant_id}"))
        db.commit()
        yield db
    finally:
        db.close()
