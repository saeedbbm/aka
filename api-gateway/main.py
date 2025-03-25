from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="API Gateway")

@app.get("/ping")
def ping():
    return {"status": "gateway ok"}

@app.post("/ingest")
async def proxy_ingest(request: Request, tenant_id: str = Header(..., alias="X-Tenant-ID")):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://data-service:8000/ingest", json=data,
                                 headers={"X-Tenant-ID": tenant_id})
    return JSONResponse(status_code=resp.status_code, content=resp.json())

@app.post("/predict")
async def proxy_predict(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://ml-service:8000/predict", json=data)
    return JSONResponse(status_code=resp.status_code, content=resp.json())
