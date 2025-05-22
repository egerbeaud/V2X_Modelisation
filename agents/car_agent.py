from typing import List, Tuple
from mesa import Agent
from abc import ABC
import random
import networkx as nx

from typing import TYPE_CHECKING

from agents.traffic_light_agent import TrafficLightAgent
if TYPE_CHECKING:
    from model import TrafficSimulationModel


class CarAgent(Agent, ABC):

    def __init__(self, unique_id: int, model: "TrafficSimulationModel", path: List[Tuple[float, float]]) -> None:
        super().__init__(unique_id, model)

        # Movement
        self.path: List[Tuple[float, float]] = path
        self.current_index: int = 0
        self.speed: float = 1.0
        self.reached_destination: bool = False

    def get_path(self) -> List[Tuple[float, float]]:
        return self.path
    
    def get_current_index(self) -> int:
        return self.current_index
    
    def get_speed(self) -> float:
        return self.speed
    
    def get_id(self) -> int:
        return self.unique_id
        


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
        x, y = self.get_position()

        if self.current_index < len(self.path) - 1:
            current_edge = (
                self.path[self.current_index],
                self.path[self.current_index + 1]
            )

            for agent in self.model.schedule.agents:  
                if isinstance(agent, TrafficLightAgent):
                    if current_edge in agent.controlled_edges and agent.is_red():
                        return

            self.current_index += 1
        else:
            self.reached_destination = True
            self.assign_new_path()


    def get_position(self) -> Tuple[float, float]:
        return self.path[self.current_index]