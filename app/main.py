from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import company, document

app = FastAPI(title="AridosCo API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(company.router)
app.include_router(document.router)

@app.get("/")
def root():
    return {"status": "ok"}
