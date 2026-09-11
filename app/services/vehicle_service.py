from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate

VALID_CAPACITIES = {
    "Volqueta": [6, 8, 10, 14, 16],
    "Patineta": [13, 14], #Obras urbanas o vias secundarias
    "Mula": [20, 21, 22, 23] #Vias nacionales
}


def validate_capacity(data: VehicleCreate):
    allowed = VALID_CAPACITIES.get(data.type)
    if allowed is None:
        raise ValueError(f"Unknown vehicle type: {data.type}")
    if int(data.capacity_m3) not in allowed:
        raise ValueError(
            f"Invalid capacity for {data.type}. Allowed values: {allowed}"
        )


def get_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.is_active == True).all()


def get_vehicle_by_id(db: Session, vehicle_id: UUID) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def create_vehicle(db: Session, vehicle: VehicleCreate) -> Vehicle:
    validate_capacity(vehicle)
    new_vehicle = Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle


def edit_vehicle(db: Session, vehicle_id: UUID, vehicle: VehicleCreate) -> Optional[Vehicle]:
    vehicle_exists = get_vehicle_by_id(db, vehicle_id)
    if not vehicle_exists:
        return None

    validate_capacity(vehicle)

    for key, value in vehicle.model_dump().items():
        setattr(vehicle_exists, key, value)
    db.commit()
    db.refresh(vehicle_exists)
    return vehicle_exists


def deactivate_vehicle(db: Session, vehicle_id: UUID) -> Optional[Vehicle]:
    vehicle = get_vehicle_by_id(db, vehicle_id)

    if not vehicle:
        return None
    
    vehicle.is_active = False
    db.commit()
    return vehicle