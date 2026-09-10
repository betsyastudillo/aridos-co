from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import company, document, auth, user

app = FastAPI(title="AridosCo API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(company.router)
app.include_router(document.router)
app.include_router(auth.router)
# app.include_router(user.router)

@app.get("/")
def root():
    return {"status": "ok"}
