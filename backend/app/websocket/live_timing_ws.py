# backend/app/websocket/live_timing_ws.py
from fastapi import APIRouter, WebSocket
import asyncio
import json
from app.services.simulator import RaceSimulator
from app.models import Track

router = APIRouter()
simulator = RaceSimulator()

@router.websocket("/ws/live-timing")
async def live_timing(websocket: WebSocket):
    await websocket.accept()
    print("✅ Cliente conectado ao WebSocket")
    
    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                data = json.loads(message)
                
                if data.get("command") == "qualify":
                    track = data.get("track")
                    if track:
                        simulator.set_track(Track(track))
                        await websocket.send_json({"status": "qualifying", "track": track})
                        print(f"🏁 Qualificação iniciada para: {track}")
                        
                elif data.get("command") == "start":
                    event = simulator.start_race()
                    if event:
                        await websocket.send_json({"status": "started", "event": event})
                        print("🏁 Corrida iniciada!")
                        
                elif data.get("command") == "skip":
                    event = simulator.skip_race()
                    if event:
                        await websocket.send_json({"status": "skipped", "event": event})
                        print("⏭️ Corrida pulada!")
                        
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")
            
            update = await simulator.generate_update()
            
            data = {
                "lap": update.lap,
                "total_laps": update.total_laps,
                "timestamp": update.timestamp.isoformat(),
                "race_status": update.race_status,
                "safety_car": update.safety_car,
                "winner": update.winner,
                "qualifying_data": update.qualifying_data if update.qualifying_data else None,
                "drivers": [
                    {
                        "position": d.position,
                        "driver": d.driver_code,
                        "driver_name": d.driver_name,
                        "team": d.team,
                        "gap": d.gap_to_leader,
                        "interval": d.interval,
                        "tyre": d.tyre.value,
                        "tyre_age": d.tyre_age,
                        "laps_completed": d.laps_completed,
                        "status": d.status.value,
                        "last_lap_time": d.last_lap_time,
                        "fastest_lap": d.fastest_lap
                    }
                    for d in update.drivers
                ],
                "events": [
                    {
                        "type": e["type"],
                        "driver": e["driver"],
                        "lap": e["lap"],
                        "description": e["description"]
                    }
                    for e in (update.events or [])
                ]
            }
            
            await websocket.send_json(data)
            
            await asyncio.sleep(2)  # Mudado para 2 segundos
            
    except Exception as e:
        print(f"❌ Erro no WebSocket: {e}")
    finally:
        print("👋 Cliente desconectado")