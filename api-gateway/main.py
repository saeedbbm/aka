import os
from fastapi import FastAPI, APIRouter, Request, Header
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="API Gateway")

# Create an APIRouter for public endpoints under a common prefix
api_router = APIRouter()

# Get service URLs from environment variables, with defaults for local testing.
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://akasa-data-service:8000")
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://akasa-ml-service:8000")

@api_router.get("/ping")
def ping():
    return {"status": "gateway ok-tested"}

@api_router.post("/ingest")
async def proxy_ingest(request: Request, tenant_id: str = Header(..., alias="X-Tenant-ID")):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        # Use the environment variable for the data service URL.
        resp = await client.post(f"{DATA_SERVICE_URL}/data/ingest", json=data,
                                 headers={"X-Tenant-ID": tenant_id})
    return JSONResponse(status_code=resp.status_code, content=resp.json())

@api_router.post("/predict")
async def proxy_predict(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        # Use the environment variable for the ML service URL.
        resp = await client.post(f"{ML_SERVICE_URL}/ml/predict", json=data)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

# Include the router with the "/api" prefix so that all routes are accessible under /api
app.include_router(api_router, prefix="/api")