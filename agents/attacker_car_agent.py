from agents.connected_car_agent import ConnectedCarAgent
from interfaces.vanetAgent import VANETAgent
import random

class AttackerCarAgent(ConnectedCarAgent):
    def __init__(self, unique_id, model, path):
        super().__init__(unique_id, model, path)

    def step(self):
        super().step()

        # Envoi systématique d’un message mensonger (fake)
        fake_messages = [
            "Fatal accident ahead",
            "Dense fog on the bridge",
            "Heavy congestion at the exit",
            "Police radar detected",
        ]
        content = random.choice(fake_messages)
        msg_type = "demn"

        fake_message = self.communicationHandler.create_message(
            content=content,
            msg_type=msg_type,
            is_fake=True
        )
        super().send_message(fake_message)

    def is_attacker(self) -> str:
        return True