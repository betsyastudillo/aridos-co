from decimal import Decimal

TRANSPORT_FLAT_RATES = {
    "volqueta": Decimal("400000"),
    "patineta": Decimal("600000"),
    "mula": Decimal("800000"),
}

def get_transport_cost(vehicle_type: str) -> Decimal:
    if vehicle_type not in TRANSPORT_FLAT_RATES:
        raise ValueError(f"No transport rate defined for vehicle type: {vehicle_type}")
    return TRANSPORT_FLAT_RATES[vehicle_type]