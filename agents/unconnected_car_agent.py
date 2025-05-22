from typing import List, Tuple
from agents.car_agent import CarAgent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import TrafficSimulationModel

    
class UnconnectedCarAgent(CarAgent):
    def __init__(self, unique_id, model: "TrafficSimulationModel", path: List[Tuple[float, float]]):
        super().__init__(unique_id, model, path)