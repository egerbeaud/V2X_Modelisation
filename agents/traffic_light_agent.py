from typing import List, Tuple
from mesa import Agent
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import TrafficSimulationModel


class TrafficLightAgent(Agent):
    def __init__(self, unique_id: int, model: "TrafficSimulationModel", position: Tuple[float, float], state:str):
        super().__init__(unique_id, model)
        self.position = position 
        self.state = state     
        self.cycle_length = random.randint(5,20)
        self.steps_since_change = 0    
        self.controlled_edges: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []

    def get_id(self) -> int:
        return self.unique_id


    def step(self):
        self.steps_since_change += 1
        if self.steps_since_change >= self.cycle_length:
            self.change_state()
            self.steps_since_change = 0


    def change_state(self):
        if self.is_red():
            self.state = "green"
        else:
            self.state = "red"


    def is_red(self) -> bool:
        return self.state == "red"

    def get_position(self) -> Tuple[float, float]:
        return self.position
