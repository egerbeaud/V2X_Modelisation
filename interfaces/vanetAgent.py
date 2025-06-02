
from abc import ABC, abstractmethod

class VANETAgent(ABC):

    @abstractmethod
    def send_message(self, message: dict):
        """
        Send a message to other agents.
        """
        raise NotImplementedError
    
    @abstractmethod
    def receive_message(self, message: dict):
        """
        Receive a message from other agents.
        """
        raise NotImplementedError

    @abstractmethod
    def send_cam(self):
        """
        Send a CAM (Cooperative Awareness Message) to other agents.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_id(self) -> int:
        """
        Get the unique identifier of the agent.
        """
        raise NotImplementedError

    @abstractmethod
    def get_speed(self) -> float:
        """
        Get the current speed of the agent.
        """
        raise NotImplementedError
    
    # @abstractmethod
    # def get_position(self) -> tuple:
    #     """
    #     Get the current position of the agent.
    #     """
    #     raise NotImplementedError
    
    @abstractmethod
    def get_sirHandler(self):
        """
        Get the SIR handler for managing infection states.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_reputation(self) -> float:
        """
        Get the current reputation of the agent.
        """
        raise NotImplementedError
    
    @abstractmethod
    def set_reputation(self, reputation: float):
        """
        Set the reputation of the agent.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_communicationHandler(self):
        """
        Get the communication handler for managing messages and CAMs.
        """
        raise NotImplementedError
    