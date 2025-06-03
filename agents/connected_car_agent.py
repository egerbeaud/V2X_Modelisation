from typing import List, Tuple
import random
from agents.car_agent import CarAgent
from communication.communication_handler import CommunicationHandler
from interfaces.vanetAgent import VANETAgent
from behaviour.sir_handler import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import TrafficSimulationModel



class ConnectedCarAgent(CarAgent):
    def __init__(self, unique_id, model: "TrafficSimulationModel", path: List[Tuple[float, float]]):
        super().__init__(unique_id, model, path)

        self.communicationHandler = CommunicationHandler(self, model)
        self.sir = SirHandler(agent_id=self.unique_id)
        self.reputation = 1.0

    def get_id(self) -> int:
        return self.unique_id
    
    
    def get_sirHandler(self) -> SirHandler:
        return self.sir
    
    def get_reputation(self) -> float:
        return self.reputation
    
    def set_reputation(self, reputation: float):
        self.reputation = reputation

    def get_communicationHandler(self) -> CommunicationHandler:
        return self.communicationHandler
    
    def send_message(self, message: dict):
        self.communicationHandler.send_message(message)

    def receive_message(self, message: dict):
        self.communicationHandler.receive_message(message)

    def send_cam(self):
        self.communicationHandler.send_cam()

    def step(self):
        super().step()

        self.send_cam()

        self.sir.update()

    def fake_message_received(self):
        if self.sir.is_infected():
            print(f"[🤒 Already infected] Agent {self.get_id()} received another fake message.")
        self.sir.infect()

# Give the VANETAgent type to the ConnectedCarAgent class. Useful for the "polymorphism".
VANETAgent.register(ConnectedCarAgent)