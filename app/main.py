from fastapi import FastAPI
from app.routers import company

app = FastAPI(title="AridosCo API")

app.include_router(company.router)

@app.get("/")
def root():
    return {"status": "ok"}
