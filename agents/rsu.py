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

        # Send a message randomly with a 20% chance
        if random.random() < 0.2:
            message_types = [
                ("Accident reported ahead", "demn", False),  
                ("Fatal accident on the ring road", "demn", True),  
                
                ("Road is completely free", "info", False),
                
                ("Heavy traffic congestion detected", "demn", False),  
                ("Slowdown alert", "info", False),  
                
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


        self.sir.update()
    


VANETAgent.register(RSUAgent)
