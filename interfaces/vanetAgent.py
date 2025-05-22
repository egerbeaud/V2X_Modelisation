
from abc import ABC

class VANETAgent(ABC):


    def send_message(self, message: dict):
        """
        Send a message to other agents.
        """
        raise NotImplementedError

    def receive_message(self, message: dict):
        """
        Receive a message from other agents.
        """
        raise NotImplementedError

    def send_cam(self):
        """
        Send a CAM (Cooperative Awareness Message) to other agents.
        """
        raise NotImplementedError
    
    def get_id(self) -> int:
        raise NotImplementedError
