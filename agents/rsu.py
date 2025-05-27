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

    def get_id(self) -> int:
        return self.unique_id

    def get_position(self) -> tuple:
        return self.position

    def send_message(self, message: dict):
        self.communicationHandler.send_message(message) 
        

    def receive_message(self, message: dict):
        self.communicationHandler.receive_message(message)

    def send_cam(self):
        self.communicationHandler.send_cam()

    def get_speed(self):
        return 0.0
    
    def fake_message_received(self):
        self.sir.infect()
    
    def step(self):
        self.send_cam()

        if random.random() < 0.2:
            message_types = [
                ("Slowdown alert", "info"),
                ("Emergency braking detected", "bsm"),
                ("Accident reported in the right-hand lane", "demn"),
                ("Area of dense fog", "demn"),
                ("Police radar control just after the tunnel", "fake"),
                ("Fatal accident on the ring road", "fake"),
            ]

            content, msg_type = random.choice(message_types)
            message = self.communicationHandler.create_message(content, msg_type)
            self.communicationHandler.send_message(message)


        self.sir.update()
    


VANETAgent.register(RSUAgent)
