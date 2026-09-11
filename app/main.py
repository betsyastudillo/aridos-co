from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import company, document, auth, user, material, order, vehicle, carrier

app = FastAPI(title="AridosCo API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(company.router)
app.include_router(document.router)
app.include_router(auth.router)
# app.include_router(user.router)
app.include_router(material.router)
app.include_router(order.router)
app.include_router(vehicle.router)
app.include_router(carrier.router)

@app.get("/")
def root():
    return {"status": "ok"}
