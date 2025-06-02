import random
from mesa import Agent
from typing import TYPE_CHECKING
from behaviour.sir_handler import SirHandler
from interfaces.vanetAgent import VANETAgent
from communication.communication_handler import CommunicationHandler

if TYPE_CHECKING:
    from model import RoadModel


class RSUAgent(Agent, VANETAgent):
    def __init__(self, unique_id: int, model: "RoadModel", position: tuple, communication_range : float):
        super().__init__(unique_id, model)
        self.position = position
        self.communicationHandler = CommunicationHandler(self, model)
        self.sir = SirHandler(agent_id=self.unique_id)
        self.communication_range = communication_range
        self.reputation = 1.0

    def get_id(self) -> int:
        return self.unique_id
    
    def get_position(self) -> tuple[float, float]:
        return self.position
    
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

    def get_speed(self):
        return 0.0
    
    def get_speed_kmh(self):
        return 0.0
    
    def fake_message_received(self):
        self.sir.infect()
    
    def step(self):
        self.send_cam()

        self.sir.update()
    


VANETAgent.register(RSUAgent)
