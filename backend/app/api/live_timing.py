# backend/app/api/live_timing.py
from fastapi import APIRouter
from app.services.simulator import RaceSimulator

router = APIRouter()

simulator = RaceSimulator()

@router.get("/live-timing")
def get_live_timing():
    return [
        {
            "position": data["position"],
            "driver": data["driver_code"],
            "driver_name": data["driver_name"],
            "gap": data["gap_to_leader"],
            "tyre": data["tyre"].value if data["tyre"] is not None else "N/A",
            "tyre_age": data["tyre_age"],
            "laps": simulator.lap
        }
        for data in sorted(simulator.positions.values(), key=lambda x: x["position"])
    ]