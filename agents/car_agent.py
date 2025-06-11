from typing import List, Tuple
from mesa import Agent
from abc import ABC
import random
import networkx as nx

from typing import TYPE_CHECKING

from agents.traffic_light_agent import TrafficLightAgent
if TYPE_CHECKING:
    from model import TrafficSimulationModel

METER_PER_EDGE = 123  # moyenne mesurée
SECONDS_PER_STEP = 1  # un pas de simulation = 1 seconde



class CarAgent(Agent, ABC):

    def __init__(self, unique_id: int, model: "TrafficSimulationModel", path: List[Tuple[float, float]]) -> None:
        super().__init__(unique_id, model)

        # Movement
        self.path: List[Tuple[float, float]] = path
        self.current_index: int = 0
        self.speed = round(random.uniform(0.15, 0.2), 2)
        self.reached_destination: bool = False
        self.virtual_position = 0.0  # position continue sur le path


    def get_path(self) -> List[Tuple[float, float]]:
        return self.path
    
    def get_current_index(self) -> int:
        return self.current_index
    
    def get_speed(self) -> float:
        return self.speed
    
    def get_id(self) -> int:
        return self.unique_id
        
    def get_speed_kmh(self):
        m_per_s = self.speed * METER_PER_EDGE  # ou utiliser une constante globale
        return round(m_per_s * 3.6, 2)



    def assign_new_path(self):
        nodes = list(self.model.road_graph.nodes) 
        start = self.path[self.current_index]

        max_attempts = 20
        attempts = 0

        while attempts < max_attempts:
            end = random.choice(nodes)
            if end == start:
                continue

            try:
                path = nx.shortest_path(
                    self.model.road_graph,  
                    source=start,
                    target=end,
                    weight="weight"
                )
                self.path = path  
                self.current_index = 0
                self.reached_destination = False
                return
            except nx.NetworkXNoPath:
                attempts += 1



    def step(self):

        draw = random.random()

        if draw < 0.05:
            # Cas d'arrêt brutal (ex : feu, bouchon)
            self.speed = 0.0
            return
        elif draw < 0.35:
            # Ralentissement léger
            self.speed = max(0.0, round(self.speed - random.uniform(0.01, 0.03), 3))
        elif draw < 0.65:
            # Accélération légère
            self.speed = min(0.3, round(self.speed + random.uniform(0.01, 0.05), 3))


        if self.speed == 0.0:
            if random.random() < 0.7:
                self.speed = round(random.uniform(0.05, 0.1), 2)
            else:
                return

        if self.current_index < len(self.path) - 1:
            current_edge = (
                self.path[self.current_index],
                self.path[self.current_index + 1]
            )

            # traffic lights check
            for agent in self.model.schedule.agents:
                if isinstance(agent, TrafficLightAgent):
                    if current_edge in agent.controlled_edges and agent.is_red():
                        self.speed = 0.0
                        return


            # Advance according to speed
            self.virtual_position += self.speed

            # Tant qu'on a passé un "segment" entier, on avance
            while self.virtual_position >= 0.5 and self.current_index < len(self.path) - 1:
                self.current_index += 1
                self.virtual_position -= 1.0

        else:
            self.reached_destination = True
            self.assign_new_path()



    def get_position(self) -> Tuple[float, float]:
        return self.path[self.current_index]