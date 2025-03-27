from fastapi import FastAPI, Depends, Header, HTTPException
import models
import crud
import db
import schemas
from fastapi import APIRouter

app = FastAPI(title="Data Service")
api_router = APIRouter()

@api_router.get("/ping")
def ping():
    return {"status": "ok"}

@api_router.post("/ingest")
def ingest_record(record: schemas.RecordCreate, tenant_id: str = Header(..., alias="X-Tenant-ID"),
                  session=Depends(db.get_session)):
    try:
        new_id = crud.save_record(session, record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"msg": "ingested", "record_id": new_id}

app.include_router(api_router, prefix="/data")