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

        # SIR
        self.sir = SirHandler(agent_id=self.unique_id)

    def get_id(self) -> int:
        return self.unique_id
    
    
    def send_message(self, message: dict):
        self.communicationHandler.send_message(message)

    def receive_message(self, message: dict):
        self.communicationHandler.receive_message(message)

    def send_cam(self):
        self.communicationHandler.send_cam()

    def step(self):
        super().step()

        self.communicationHandler.send_cam()

        self.sir.update()


        # Send a message randomly with a 20% chance
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

    def fake_message_received(self):
        self.sir.infect()

# Give the VANETAgent type to the ConnectedCarAgent class. Useful for the "polymorphism".
VANETAgent.register(ConnectedCarAgent)