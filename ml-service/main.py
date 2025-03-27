from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import model
from fastapi import APIRouter

app = FastAPI(title="ML Service")
api_router = APIRouter()

@api_router.get("/ping")
def ping():
    return {"status": "ok"}

class NoteInput(BaseModel):
    note: str

@api_router.post("/predict")
def predict_icd(data: NoteInput):
    try:
        prediction = model.predict(data.note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"icd10_code": prediction}

app.include_router(api_router, prefix="/ml")