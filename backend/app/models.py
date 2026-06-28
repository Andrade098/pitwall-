# backend/app/models.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

class TyreType(str, Enum):
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"

class DriverStatus(str, Enum):
    RACING = "RACING"
    PIT = "PIT"
    OUT = "OUT"
    SAFETY_CAR = "SAFETY_CAR"
    STARTING = "STARTING"
    FINISHED = "FINISHED"

class Track(str, Enum):
    BAHRAIN = "bahrain"
    JEDDAH = "jeddah"
    MELBOURNE = "melbourne"
    SUZUKA = "suzuka"
    SHANGHAI = "shanghai"
    MIAMI = "miami"
    IMOLA = "imola"
    MONACO = "monaco"
    MONTREAL = "montreal"
    BARCELONA = "barcelona"
    SILVERSTONE = "silverstone"
    SPA = "spa"
    HUNGARORING = "hungaroring"
    ZANDVOORT = "zandvoort"
    MONZA = "monza"
    SINGAPORE = "singapore"
    COTA = "cota"
    MEXICO = "mexico"
    SAO_PAULO = "sao_paulo"
    LAS_VEGAS = "las_vegas"
    QATAR = "qatar"
    ABU_DHABI = "abu_dhabi"

class TrackInfo(BaseModel):
    name: str
    country: str
    laps: int
    safety_car_chance: float
    description: str

class DriverPosition(BaseModel):
    position: int
    driver_code: str
    driver_name: str
    team: str
    gap_to_leader: str
    interval: Optional[str] = None
    tyre: TyreType
    tyre_age: int
    laps_completed: int
    status: DriverStatus = DriverStatus.RACING
    sector1: Optional[float] = None
    sector2: Optional[float] = None
    sector3: Optional[float] = None
    last_lap_time: Optional[str] = None
    fastest_lap: bool = False
    points: int = 0

class RaceUpdate(BaseModel):
    lap: int
    total_laps: int
    timestamp: datetime
    drivers: list[DriverPosition]
    events: Optional[list[dict]] = None
    race_status: str
    safety_car: bool = False
    winner: Optional[str] = None
    qualifying_data: Optional[list] = None

class RaceEvent(BaseModel):
    type: str
    driver: str
    lap: int
    description: str