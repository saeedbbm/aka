from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import model

app = FastAPI(title="ML Service")

@app.get("/ping")
def ping():
    return {"status": "ok"}

class NoteInput(BaseModel):
    note: str

@app.post("/predict")
def predict_icd(data: NoteInput):
    try:
        prediction = model.predict(data.note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"icd10_code": prediction}
