# backend/app/services/simulator.py
import random
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from app.models import DriverPosition, RaceUpdate, TyreType, DriverStatus, Track
from app.tracks import TRACKS, DRIVERS_2026

class RaceSimulator:
    def __init__(self):
        self.track = None
        self.drivers_config = DRIVERS_2026
        self.positions: Dict[str, dict] = {}
        self.lap = 0
        self.total_laps = 0
        self.tyre_types = [TyreType.SOFT, TyreType.MEDIUM, TyreType.HARD]
        self.race_status = "waiting"
        self.safety_car = False
        self.safety_car_laps = 0
        self.winner = None
        self.starting_grid = []
        self.race_started = False
        self.lap_time_seconds = 2  # Mudado para 2 segundos

    def reset_race(self):
        """Reseta a corrida para o estado inicial"""
        self.lap = 0
        self.race_status = "waiting"
        self.safety_car = False
        self.safety_car_laps = 0
        self.winner = None
        self.race_started = False
        self.positions = {}
        self.starting_grid = []
        self.total_laps = 0

    def set_track(self, track: Track):
        """Define a pista para a corrida"""
        self.reset_race()
        self.track = track
        self.total_laps = TRACKS[track].laps
        self.race_status = "qualifying"
        self.generate_qualifying()

    def generate_qualifying_time(self, performance: float, session: int) -> float:
        """Gera um tempo de classificação realista"""
        base_time = 75.0 - (session - 1) * 0.300
        perf_factor = 1.0 / performance
        variation = random.uniform(0, 0.800) + random.uniform(0, 0.300)
        total = base_time * perf_factor + variation
        return total

    def format_qualy_time(self, time_value) -> str:
        """Formata tempo de classificação para mm:ss.xxx"""
        if time_value is None or time_value == "-":
            return "-"
        try:
            minutes = int(time_value // 60)
            seconds = time_value % 60
            return f"{minutes}:{seconds:06.3f}"
        except:
            return "-"

    def generate_qualifying(self):
        """Gera o grid de largada com tempos de Q1, Q2, Q3"""
        drivers_with_qualy = []
        
        for driver in self.drivers_config:
            base_perf = driver["performance"]
            
            # Q1 - todos participam
            q1_time = self.generate_qualifying_time(base_perf, 1)
            
            # Q2 - apenas top 15 (75% dos pilotos)
            q2_time = None
            if random.random() < 0.75:
                q2_time = self.generate_qualifying_time(base_perf, 2)
            
            # Q3 - apenas top 10 (67% dos que passaram)
            q3_time = None
            if q2_time and random.random() < 0.67:
                q3_time = self.generate_qualifying_time(base_perf, 3)
            
            # Melhor tempo é o mais rápido entre os disponíveis
            times = []
            if q1_time is not None:
                times.append(q1_time)
            if q2_time is not None:
                times.append(q2_time)
            if q3_time is not None:
                times.append(q3_time)
            
            best_time = min(times) if times else q1_time
            
            drivers_with_qualy.append({
                "driver": driver,
                "q1": q1_time,
                "q2": q2_time,
                "q3": q3_time,
                "best_time": best_time,
                "performance": base_perf,
                "passed_q2": q2_time is not None,
                "passed_q3": q3_time is not None
            })
        
        # Ordenar por melhor tempo
        sorted_drivers = sorted(
            drivers_with_qualy,
            key=lambda x: x["best_time"]
        )
        
        self.starting_grid = []
        for i, driver_data in enumerate(sorted_drivers):
            self.starting_grid.append({
                "position": i + 1,
                "driver_code": driver_data["driver"]["code"],
                "driver_name": driver_data["driver"]["name"],
                "team": driver_data["driver"]["team"],
                "team_short": driver_data["driver"]["team_short"],
                "performance": driver_data["driver"]["performance"],
                "q1": self.format_qualy_time(driver_data["q1"]),
                "q2": self.format_qualy_time(driver_data["q2"]) if driver_data["passed_q2"] else "-",
                "q3": self.format_qualy_time(driver_data["q3"]) if driver_data["passed_q3"] else "-",
                "best_time": self.format_qualy_time(driver_data["best_time"]),
                "passed_q2": driver_data["passed_q2"],
                "passed_q3": driver_data["passed_q3"]
            })
        
        # Inicializar posições com o grid (sem pneus ainda)
        self.positions = {}
        for i, driver_data in enumerate(self.starting_grid):
            # Pneus só serão definidos na largada
            self.positions[driver_data["driver_code"]] = {
                "driver_code": driver_data["driver_code"],
                "driver_name": driver_data["driver_name"],
                "team": driver_data["team"],
                "team_short": driver_data["team_short"],
                "position": i + 1,
                "gap_to_leader": "+0.000" if i == 0 else f"+{i * 0.400:.3f}",
                "interval": None if i == 0 else f"+{i * 0.400:.3f}",
                "tyre": None,  # Será definido na largada
                "tyre_age": 0,
                "laps_completed": 0,
                "status": DriverStatus.STARTING,
                "last_lap_time": "0:00.000",
                "fastest_lap": False,
                "base_performance": driver_data["performance"] + random.uniform(-0.02, 0.02),
                "points": 0,
                "finished": False,
                "q1_time": driver_data["q1"],
                "q2_time": driver_data["q2"],
                "q3_time": driver_data["q3"],
                "best_qualy_time": driver_data["best_time"],
                "passed_q2": driver_data["passed_q2"],
                "passed_q3": driver_data["passed_q3"]
            }

    def get_tyre_performance(self, tyre: TyreType) -> float:
        """Retorna o multiplicador de performance para cada tipo de pneu"""
        if tyre == TyreType.SOFT:
            return 1.05  # Mais rápido
        elif tyre == TyreType.MEDIUM:
            return 1.00  # Neutro
        elif tyre == TyreType.HARD:
            return 0.95  # Mais lento
        return 1.00

    def get_tyre_degradation(self, tyre: TyreType, age: int) -> float:
        """Calcula a degradação do pneu baseado no tipo e idade"""
        if tyre == TyreType.SOFT:
            # Macio degrada rápido (começa a perder performance com 8 voltas)
            if age <= 8:
                return 0.0
            else:
                return (age - 8) * 0.015  # Perde 1.5% por volta
        elif tyre == TyreType.MEDIUM:
            # Médio degrada moderadamente (começa com 15 voltas)
            if age <= 15:
                return 0.0
            else:
                return (age - 15) * 0.010  # Perde 1% por volta
        elif tyre == TyreType.HARD:
            # Duro degrada lentamente (começa com 25 voltas)
            if age <= 25:
                return 0.0
            else:
                return (age - 25) * 0.005  # Perde 0.5% por volta
        return 0.0

    def get_tyre_pit_window(self, tyre: TyreType) -> int:
        """Retorna a janela de pit stop ideal para cada pneu"""
        if tyre == TyreType.SOFT:
            return random.randint(10, 18)  # Para entre 10-18 voltas
        elif tyre == TyreType.MEDIUM:
            return random.randint(18, 28)  # Para entre 18-28 voltas
        elif tyre == TyreType.HARD:
            return random.randint(28, 40)  # Para entre 28-40 voltas
        return 20

    def generate_lap_time(self, position: int, performance: float, tyre: TyreType, tyre_age: int) -> str:
        """Gera um tempo de volta realista baseado na performance do carro e pneu"""
        base = 80
        
        # Performance base do carro
        perf_factor = 1.0 / performance
        
        # Performance do pneu
        tyre_perf = self.get_tyre_performance(tyre)
        
        # Degradação do pneu
        degradation = self.get_tyre_degradation(tyre, tyre_age)
        
        # Fator final (quanto maior, mais lento)
        total_factor = perf_factor * (1.0 / tyre_perf) * (1.0 + degradation)
        
        variation = random.uniform(0, 1.5) + (position * 0.1 * total_factor)
        total = base * total_factor + variation
        
        minutes = int(total // 60)
        seconds = total % 60
        return f"{minutes}:{seconds:06.3f}"

    def calculate_gaps(self):
        """Calcula os gaps entre os pilotos"""
        active_drivers = [
            d for d in self.positions.values() 
            if d["status"] != DriverStatus.OUT
        ]
        
        sorted_positions = sorted(active_drivers, key=lambda x: x["position"])
        
        if not sorted_positions:
            return
            
        leader = sorted_positions[0]
        leader["gap_to_leader"] = "+0.000"
        leader["interval"] = None
        
        for i, driver in enumerate(sorted_positions[1:], 1):
            gap = i * 0.400 + random.uniform(-0.200, 0.200)
            driver["gap_to_leader"] = f"+{gap:.3f}"
            
            prev_driver = sorted_positions[i - 1]
            interval = random.uniform(0.300, 1.200)
            driver["interval"] = f"+{interval:.3f}"

    def generate_events(self) -> List[dict]:
        """Gera eventos aleatórios da corrida"""
        events = []
        
        # Safety Car
        if self.track and random.random() < TRACKS[self.track].safety_car_chance * 0.01:
            if not self.safety_car and self.lap > 5 and self.lap < self.total_laps - 5:
                self.safety_car = True
                self.safety_car_laps = random.randint(2, 5)
                events.append({
                    "type": "SAFETY_CAR",
                    "driver": "",
                    "lap": self.lap,
                    "description": f"🚨 Safety Car acionado! (pista: {TRACKS[self.track].name})"
                })
        
        # Pit stops com lógica baseada no pneu
        for driver_code, data in self.positions.items():
            if data["status"] == DriverStatus.OUT:
                continue
            
            if data["tyre"] is None:
                continue
                
            tyre = data["tyre"]
            tyre_age = data["tyre_age"]
            pit_window = self.get_tyre_pit_window(tyre)
            
            # Verifica se está na janela de pit stop
            if tyre_age >= pit_window and random.random() < 0.15:
                current_tyre = data["tyre"]
                
                # Escolhe novo pneu (geralmente vai para o próximo mais duro)
                tyre_priority = [TyreType.SOFT, TyreType.MEDIUM, TyreType.HARD]
                current_index = tyre_priority.index(current_tyre)
                
                # Se já está no duro, pode repetir ou colocar médio
                if current_index >= 2:
                    new_tyre = random.choice([TyreType.MEDIUM, TyreType.HARD])
                else:
                    new_tyre = tyre_priority[min(current_index + 1, 2)]
                
                tyre_names = {
                    TyreType.SOFT: "macio",
                    TyreType.MEDIUM: "médio",
                    TyreType.HARD: "duro",
                    TyreType.INTERMEDIATE: "intermediário",
                    TyreType.WET: "chuva"
                }
                
                events.append({
                    "type": "PIT_STOP",
                    "driver": driver_code,
                    "lap": self.lap,
                    "description": f"🔧 {data['driver_name']} nos boxes, botou pneu {tyre_names[new_tyre]}"
                })
                
                data["tyre"] = new_tyre
                data["tyre_age"] = 0
        
        # Ultrapassagens
        if random.random() < 0.08:
            active_drivers = [d for d in self.positions.values() if d["status"] != DriverStatus.OUT]
            if len(active_drivers) >= 2:
                d1, d2 = random.sample(active_drivers, 2)
                pos1 = d1["position"]
                pos2 = d2["position"]
                if abs(pos1 - pos2) == 1:
                    events.append({
                        "type": "OVERTAKE",
                        "driver": d1["driver_code"] if pos1 < pos2 else d2["driver_code"],
                        "lap": self.lap,
                        "description": f"🏁 Ultrapassagem: {d1['driver_code']} passou {d2['driver_code']}"
                    })
                    d1["position"], d2["position"] = d2["position"], d1["position"]
        
        return events

    def recalculate_positions(self):
        """Recalcula posições baseado na performance e pneus"""
        active_drivers = [
            d for d in self.positions.values() 
            if d["status"] != DriverStatus.OUT
        ]
        
        # Calcular performance efetiva para cada piloto
        for driver in active_drivers:
            if driver["tyre"] is None:
                continue
                
            base_perf = driver["base_performance"]
            tyre_perf = self.get_tyre_performance(driver["tyre"])
            degradation = self.get_tyre_degradation(driver["tyre"], driver["tyre_age"])
            
            # Performance efetiva = base * pneu - degradação
            effective_perf = base_perf * tyre_perf * (1.0 - degradation)
            driver["effective_performance"] = effective_perf
        
        sorted_drivers = sorted(
            active_drivers,
            key=lambda x: x.get("effective_performance", 0.5) * random.uniform(0.99, 1.01),
            reverse=True
        )
        
        for i, driver in enumerate(sorted_drivers):
            driver["position"] = i + 1

    def check_race_finish(self):
        """Verifica se a corrida acabou"""
        if self.lap >= self.total_laps:
            self.finish_race()
            return True
        return False

    def finish_race(self):
        """Finaliza a corrida e define o vencedor"""
        self.race_status = "finished"
        active_drivers = [
            d for d in self.positions.values() 
            if d["status"] != DriverStatus.OUT
        ]
        if active_drivers:
            self.winner = sorted(active_drivers, key=lambda x: x["position"])[0]["driver_code"]

    def skip_race(self):
        """Pula a simulação e finaliza a corrida instantaneamente"""
        if self.race_status == "racing":
            self.lap = self.total_laps
            self.finish_race()
            return {
                "type": "RACE_SKIP",
                "driver": "",
                "lap": self.lap,
                "description": "⏭️ Corrida pulada! Resultados finais gerados!"
            }
        return None

    def calculate_performance_variation(self, driver_code: str, base_performance: float, lap: int) -> float:
        """Calcula variação de performance baseada no momento da temporada"""
        variation = 0.0
        
        if driver_code in ["ANT", "RUS"]:
            if driver_code == "ANT":
                variation += 0.02 * (1 + 0.3 * (lap % 3 == 0))
        
        elif driver_code in ["HAM", "LEC"]:
            variation += 0.01 * (lap % 5 < 3) - 0.01 * (lap % 5 >= 3)
        
        elif driver_code in ["NOR", "PIA", "VER", "HAD"]:
            variation += 0.005 * (1 if driver_code in ["NOR", "VER"] else -1)
            
        return base_performance + variation

    def start_race(self):
        """Inicia a corrida - define os pneus iniciais"""
        if self.race_status == "qualifying":
            self.race_status = "racing"
            self.race_started = True
            self.lap = 0
            
            # Define pneus para cada piloto baseado na posição
            for i, data in enumerate(self.positions.values()):
                # Pilotos no top 10 tendem a usar pneus mais macios
                if i < 10:  # Top 10
                    tyre_choice = random.choices(
                        [TyreType.SOFT, TyreType.MEDIUM, TyreType.HARD],
                        weights=[0.6, 0.3, 0.1]
                    )[0]
                else:  # Fora do top 10
                    tyre_choice = random.choices(
                        [TyreType.SOFT, TyreType.MEDIUM, TyreType.HARD],
                        weights=[0.1, 0.4, 0.5]
                    )[0]
                
                data["tyre"] = tyre_choice
                data["tyre_age"] = 0
                data["status"] = DriverStatus.RACING
                data["laps_completed"] = 0
            
            return {
                "type": "RACE_START",
                "driver": "",
                "lap": 0,
                "description": "🏁 Bandeira Verde! Corrida iniciada!"
            }
        return None

    async def generate_update(self) -> RaceUpdate:
        """Gera uma atualização completa da corrida"""
        if self.race_status == "waiting":
            drivers_positions = []
            for i, data in enumerate(self.starting_grid[:10]):
                drivers_positions.append(DriverPosition(
                    position=i + 1,
                    driver_code=data["driver_code"],
                    driver_name=data["driver_name"],
                    team=data["team_short"],
                    gap_to_leader="+0.000" if i == 0 else f"+{i * 0.400:.3f}",
                    interval=None if i == 0 else f"+{i * 0.400:.3f}",
                    tyre=TyreType.SOFT,
                    tyre_age=0,
                    laps_completed=0,
                    status=DriverStatus.STARTING,
                    last_lap_time="0:00.000",
                    fastest_lap=False
                ))
            
            return RaceUpdate(
                lap=0,
                total_laps=self.total_laps,
                timestamp=datetime.now(),
                drivers=drivers_positions,
                events=[],
                race_status=self.race_status,
                safety_car=False
            )

        if self.race_status == "qualifying":
            drivers_positions = []
            for data in self.starting_grid:
                drivers_positions.append(DriverPosition(
                    position=data["position"],
                    driver_code=data["driver_code"],
                    driver_name=data["driver_name"],
                    team=data["team_short"],
                    gap_to_leader="+0.000" if data["position"] == 1 else f"+{(data['position']-1) * 0.400:.3f}",
                    interval=None if data["position"] == 1 else f"+{random.uniform(0.2, 0.8):.3f}",
                    tyre=TyreType.SOFT,  # Placeholder, não usado na classificação
                    tyre_age=0,
                    laps_completed=0,
                    status=DriverStatus.STARTING,
                    last_lap_time=data["best_time"],
                    fastest_lap=data["position"] == 1
                ))
            
            return RaceUpdate(
                lap=0,
                total_laps=self.total_laps,
                timestamp=datetime.now(),
                drivers=drivers_positions,
                events=[{
                    "type": "QUALIFYING_RESULT",
                    "driver": "",
                    "lap": 0,
                    "description": "🏁 Classificação finalizada! Ordem de largada definida."
                }],
                race_status=self.race_status,
                safety_car=False,
                qualifying_data=self.starting_grid
            )

        if self.race_status == "racing":
            self.lap += 1
            
            for driver in self.positions.values():
                if driver["status"] == DriverStatus.OUT:
                    continue
                    
                driver["base_performance"] = self.calculate_performance_variation(
                    driver["driver_code"], 
                    driver["base_performance"], 
                    self.lap
                )
                driver["base_performance"] = max(0.80, min(1.10, driver["base_performance"]))
                
                # Aumentar idade do pneu
                if driver["tyre"] is not None:
                    driver["tyre_age"] += 1
                    
                    # Se o pneu estiver muito velho, pode causar problemas
                    tyre_degradation = self.get_tyre_degradation(driver["tyre"], driver["tyre_age"])
                    if tyre_degradation > 0.25:  # Mais de 25% de degradação
                        if random.random() < 0.02:  # 2% de chance de abandonar
                            driver["status"] = DriverStatus.OUT
                            events.append({
                                "type": "RETIREMENT",
                                "driver": driver["driver_code"],
                                "lap": self.lap,
                                "description": f"💥 {driver['driver_name']} abandonou! (problema nos pneus)"
                            })
                
                driver["laps_completed"] += 1
                
                if driver["position"] == 1:
                    driver["gap_to_leader"] = "+0.000"
            
            self.recalculate_positions()
            self.calculate_gaps()
            
            events = self.generate_events()
            
            self.check_race_finish()
            
            if self.race_status == "finished" and self.winner:
                winner_name = self.positions[self.winner]["driver_name"]
                events.append({
                    "type": "RACE_FINISH",
                    "driver": self.winner,
                    "lap": self.lap,
                    "description": f"🏆 {winner_name} venceu a corrida!"
                })
                active_drivers = sorted(
                    [d for d in self.positions.values() if d["status"] != DriverStatus.OUT],
                    key=lambda x: x["position"]
                )
                for i, d in enumerate(active_drivers[:3]):
                    if i == 0:
                        medal = "🥇"
                    elif i == 1:
                        medal = "🥈"
                    else:
                        medal = "🥉"
                    events.append({
                        "type": "PODIUM",
                        "driver": d["driver_code"],
                        "lap": self.lap,
                        "description": f"{medal} {d['driver_name']} - P{i+1} lugar!"
                    })
            
            drivers_positions = []
            active_drivers = sorted(
                [d for d in self.positions.values()],
                key=lambda x: x["position"]
            )
            
            for driver_data in active_drivers:
                drivers_positions.append(DriverPosition(
                    position=driver_data["position"],
                    driver_code=driver_data["driver_code"],
                    driver_name=driver_data["driver_name"],
                    team=driver_data["team_short"],
                    gap_to_leader=driver_data["gap_to_leader"] if driver_data["status"] != DriverStatus.OUT else "DNF",
                    interval=driver_data.get("interval") if driver_data["status"] != DriverStatus.OUT else "-",
                    tyre=driver_data["tyre"] if driver_data["tyre"] is not None else TyreType.SOFT,
                    tyre_age=driver_data["tyre_age"] if driver_data["tyre"] is not None else 0,
                    laps_completed=driver_data["laps_completed"],
                    status=driver_data["status"],
                    last_lap_time=self.generate_lap_time(
                        driver_data["position"], 
                        driver_data["base_performance"],
                        driver_data["tyre"] if driver_data["tyre"] is not None else TyreType.SOFT,
                        driver_data["tyre_age"] if driver_data["tyre"] is not None else 0
                    ) if driver_data["status"] != DriverStatus.OUT else "DNF",
                    fastest_lap=random.random() < 0.03 and driver_data["status"] != DriverStatus.OUT
                ))
            
            return RaceUpdate(
                lap=self.lap,
                total_laps=self.total_laps,
                timestamp=datetime.now(),
                drivers=drivers_positions,
                events=events if events else None,
                race_status=self.race_status,
                safety_car=self.safety_car,
                winner=self.winner
            )
        
        if self.race_status == "finished":
            drivers_positions = []
            active_drivers = sorted(
                [d for d in self.positions.values()],
                key=lambda x: x["position"]
            )
            
            for driver_data in active_drivers:
                drivers_positions.append(DriverPosition(
                    position=driver_data["position"],
                    driver_code=driver_data["driver_code"],
                    driver_name=driver_data["driver_name"],
                    team=driver_data["team_short"],
                    gap_to_leader=driver_data["gap_to_leader"] if driver_data["status"] != DriverStatus.OUT else "DNF",
                    interval=driver_data.get("interval") if driver_data["status"] != DriverStatus.OUT else "-",
                    tyre=driver_data["tyre"] if driver_data["tyre"] is not None else TyreType.SOFT,
                    tyre_age=driver_data["tyre_age"] if driver_data["tyre"] is not None else 0,
                    laps_completed=driver_data["laps_completed"],
                    status=driver_data["status"],
                    last_lap_time="DNF" if driver_data["status"] == DriverStatus.OUT else "-",
                    fastest_lap=False
                ))
            
            return RaceUpdate(
                lap=self.total_laps,
                total_laps=self.total_laps,
                timestamp=datetime.now(),
                drivers=drivers_positions,
                events=[],
                race_status=self.race_status,
                safety_car=False,
                winner=self.winner
            )
        
        return RaceUpdate(
            lap=0,
            total_laps=self.total_laps,
            timestamp=datetime.now(),
            drivers=[],
            events=[],
            race_status=self.race_status,
            safety_car=False
        )