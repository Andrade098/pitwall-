# backend/app/tracks.py
from app.models import Track, TrackInfo

TRACKS = {
    Track.BAHRAIN: TrackInfo(
        name="Bahrain International Circuit",
        country="Bahrain",
        laps=57,
        safety_car_chance=0.3,
        description="Circuito no deserto, alta degradação de pneus"
    ),
    Track.JEDDAH: TrackInfo(
        name="Jeddah Corniche Circuit",
        country="Arábia Saudita",
        laps=50,
        safety_car_chance=0.5,
        description="Circuito urbano rápido, muitas ultrapassagens"
    ),
    Track.MELBOURNE: TrackInfo(
        name="Albert Park Circuit",
        country="Austrália",
        laps=58,
        safety_car_chance=0.4,
        description="Circuito semi-urbano, clima imprevisível"
    ),
    Track.SUZUKA: TrackInfo(
        name="Suzuka International Circuit",
        country="Japão",
        laps=53,
        safety_car_chance=0.2,
        description="Circuito clássico, curvas icônicas"
    ),
    Track.SHANGHAI: TrackInfo(
        name="Shanghai International Circuit",
        country="China",
        laps=56,
        safety_car_chance=0.3,
        description="Circuito com longas retas"
    ),
    Track.MIAMI: TrackInfo(
        name="Miami International Autodrome",
        country="EUA",
        laps=57,
        safety_car_chance=0.35,
        description="Circuito urbano, clima quente"
    ),
    Track.IMOLA: TrackInfo(
        name="Autodromo Enzo e Dino Ferrari",
        country="Itália",
        laps=63,
        safety_car_chance=0.25,
        description="Circuito histórico, curvas rápidas"
    ),
    Track.MONACO: TrackInfo(
        name="Circuit de Monaco",
        country="Mônaco",
        laps=78,
        safety_car_chance=0.8,
        description="Circuito urbano lendário, quase sem ultrapassagens"
    ),
    Track.MONTREAL: TrackInfo(
        name="Circuit Gilles Villeneuve",
        country="Canadá",
        laps=70,
        safety_car_chance=0.4,
        description="Circuito com longas retas e zonas de freada"
    ),
    Track.BARCELONA: TrackInfo(
        name="Circuit de Barcelona-Catalunya",
        country="Espanha",
        laps=66,
        safety_car_chance=0.2,
        description="Circuito de testes, todas as curvas"
    ),
    Track.SILVERSTONE: TrackInfo(
        name="Silverstone Circuit",
        country="Reino Unido",
        laps=52,
        safety_car_chance=0.3,
        description="Circuito histórico, curvas de alta velocidade"
    ),
    Track.SPA: TrackInfo(
        name="Circuit de Spa-Francorchamps",
        country="Bélgica",
        laps=44,
        safety_car_chance=0.4,
        description="Circuito nas Ardenas, clima imprevisível"
    ),
    Track.HUNGARORING: TrackInfo(
        name="Hungaroring",
        country="Hungria",
        laps=70,
        safety_car_chance=0.2,
        description="Circuito técnico, difícil ultrapassar"
    ),
    Track.ZANDVOORT: TrackInfo(
        name="Circuit Zandvoort",
        country="Holanda",
        laps=72,
        safety_car_chance=0.2,
        description="Circuito com curvas inclinadas"
    ),
    Track.MONZA: TrackInfo(
        name="Autodromo Nazionale Monza",
        country="Itália",
        laps=53,
        safety_car_chance=0.15,
        description="Templo da Velocidade, longas retas"
    ),
    Track.SINGAPORE: TrackInfo(
        name="Marina Bay Street Circuit",
        country="Singapura",
        laps=61,
        safety_car_chance=0.7,
        description="Circuito urbano noturno, alta chance de Safety Car"
    ),
    Track.COTA: TrackInfo(
        name="Circuit of the Americas",
        country="EUA",
        laps=56,
        safety_car_chance=0.3,
        description="Circuito moderno, curvas desafiadoras"
    ),
    Track.MEXICO: TrackInfo(
        name="Autodromo Hermanos Rodriguez",
        country="México",
        laps=71,
        safety_car_chance=0.25,
        description="Circuito em alta altitude"
    ),
    Track.SAO_PAULO: TrackInfo(
        name="Autodromo Jose Carlos Pace",
        country="Brasil",
        laps=71,
        safety_car_chance=0.4,
        description="Circuito histórico, clima imprevisível"
    ),
    Track.LAS_VEGAS: TrackInfo(
        name="Las Vegas Strip Circuit",
        country="EUA",
        laps=50,
        safety_car_chance=0.3,
        description="Circuito urbano noturno em Las Vegas"
    ),
    Track.QATAR: TrackInfo(
        name="Losail International Circuit",
        country="Qatar",
        laps=57,
        safety_car_chance=0.2,
        description="Circuito no deserto, pista rápida"
    ),
    Track.ABU_DHABI: TrackInfo(
        name="Yas Marina Circuit",
        country="Emirados Árabes",
        laps=58,
        safety_car_chance=0.25,
        description="Circuito moderno, corrida noturna"
    ),
}

DRIVERS_2026 = [
    {"code": "ANT", "name": "Kimi Antonelli", "team": "Mercedes", "team_short": "MER", "performance": 1.07},
    {"code": "RUS", "name": "George Russell", "team": "Mercedes", "team_short": "MER", "performance": 1.06},
    {"code": "HAM", "name": "Lewis Hamilton", "team": "Ferrari", "team_short": "FER", "performance": 1.05},
    {"code": "LEC", "name": "Charles Leclerc", "team": "Ferrari", "team_short": "FER", "performance": 1.04},
    {"code": "NOR", "name": "Lando Norris", "team": "McLaren", "team_short": "MCL", "performance": 1.03},
    {"code": "PIA", "name": "Oscar Piastri", "team": "McLaren", "team_short": "MCL", "performance": 1.01},
    {"code": "VER", "name": "Max Verstappen", "team": "Red Bull", "team_short": "RBR", "performance": 1.02},
    {"code": "HAD", "name": "Isack Hadjar", "team": "Red Bull", "team_short": "RBR", "performance": 0.99},
    {"code": "GAS", "name": "Pierre Gasly", "team": "Alpine", "team_short": "ALP", "performance": 0.93},
    {"code": "COL", "name": "Franco Colapinto", "team": "Alpine", "team_short": "ALP", "performance": 0.91},
    {"code": "SAI", "name": "Carlos Sainz", "team": "Williams", "team_short": "WIL", "performance": 0.97},
    {"code": "ALB", "name": "Alex Albon", "team": "Williams", "team_short": "WIL", "performance": 0.95},
    {"code": "LAW", "name": "Liam Lawson", "team": "RB", "team_short": "RB", "performance": 0.94},
    {"code": "LIN", "name": "Arvid Lindblad", "team": "RB", "team_short": "RB", "performance": 0.93},
    {"code": "BEA", "name": "Oliver Bearman", "team": "Haas", "team_short": "HAA", "performance": 0.92},
    {"code": "OCO", "name": "Esteban Ocon", "team": "Haas", "team_short": "HAA", "performance": 0.91},
    {"code": "HUL", "name": "Nico Hulkenberg", "team": "Audi", "team_short": "AUD", "performance": 0.90},
    {"code": "BOR", "name": "Gabriel Bortoleto", "team": "Audi", "team_short": "AUD", "performance": 0.88},
    {"code": "ALO", "name": "Fernando Alonso", "team": "Aston Martin", "team_short": "AST", "performance": 0.88},
    {"code": "STR", "name": "Lance Stroll", "team": "Aston Martin", "team_short": "AST", "performance": 0.85},
    {"code": "PER", "name": "Sergio Perez", "team": "Cadillac", "team_short": "CAD", "performance": 0.86},
    {"code": "BOT", "name": "Valtteri Bottas", "team": "Cadillac", "team_short": "CAD", "performance": 0.85},
]