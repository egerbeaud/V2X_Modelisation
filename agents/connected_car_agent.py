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


        # Send a message randomly with a 20% chance
        if random.random() < 0.2:
            message_types = [
                ("Accident reported ahead", "demn", False),  
                ("Fatal accident on the ring road", "demn", True),  
                
                ("Road is completely free", "info", False),
                
                ("Heavy traffic congestion detected", "demn", False),  
                ("Slowdown alert", "info", True),  
                
                ("Dense fog in the tunnel", "demn", True),
                ("Police radar detected after the bridge", "demn", True),
            ]

            choix = random.choice(message_types)  

            if len(choix) == 3:
                content = choix[0]
                msg_type = choix[1]
                is_fake = choix[2]
            else:
                content = choix[0]
                msg_type = choix[1]
                is_fake = False
            message = self.communicationHandler.create_message(content, msg_type, is_fake)
            self.communicationHandler.send_message(message)

    def fake_message_received(self):
        self.sir.infect()

# Give the VANETAgent type to the ConnectedCarAgent class. Useful for the "polymorphism".
VANETAgent.register(ConnectedCarAgent)