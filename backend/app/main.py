# backend/app/main.py
from fastapi import FastAPI
from app.api.live_timing import router as live_timing_router
from app.websocket.live_timing_ws import router as ws_router

app = FastAPI(
    title="PitWall API",
    version="0.1.0"
)

app.include_router(live_timing_router)
app.include_router(ws_router)

@app.get("/")
def root():
    return {
        "project": "PitWall",
        "status": "running"
    }