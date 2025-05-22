from typing import List
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import TrafficSimulationModel

from interfaces.vanetAgent import VANETAgent

from utils.driving_tools import get_distance



class CommunicationHandler:
    def __init__(self, agent: "VANETAgent", model: "TrafficSimulationModel") -> None:
        self.model = model
        self.agent = agent 
        self.last_message: str = ""
        self.seen_message_ids: set[str] = set()
        self.received_messages: list[dict] = []
        self.current_neighbors: List["VANETAgent"] = []


    def create_cam(self) -> dict:
        return {
            "id": f"cam-{uuid.uuid4()}",
            "sender_id": self.agent.get_id(), 
            "type": "cam",
            "position": self.agent.get_position(), 
            "speed": self.agent.get_speed(), 
            "step": self.model.step_count  
        }
    
    def send_cam(self):
        cam = self.create_cam()

        # Updates the list of neighbours
        self.current_neighbors = self.get_reachable_neighbors() 


        for agent in self.current_neighbors:
            print(f"[📥 CAM received by {agent.get_id()}] from {self.agent.get_id()} → Pos={cam['position']} V={cam['speed']:.2f}") 


    def send_message(self, message: dict):
        msg_id = message["id"]


        print(f"[🚗 {self.agent.get_id()}] Send the message {msg_id[:6]} (TTL={message['ttl']}) : \"{message['content']}\"")
        if not self.current_neighbors:
            print(f"(no neighbours nearby)")
            return

        for agent in self.current_neighbors:
            if msg_id in agent.communicationHandler.seen_message_ids:
                continue

            print(f"    ↳ Forwarded to {agent.unique_id} the message from {message['sender_id']}")
            agent.receive_message(message)




    def receive_message(self, message: dict):
        msg_id = message["id"]

        if msg_id in self.seen_message_ids:
            return
        self.seen_message_ids.add(msg_id)
        self.received_messages.append(message)
        self.last_message = message["content"]

        print(f"[📨 {self.agent.get_id()}] Received {msg_id[:6]} from {message['sender_id']} : {message['content']}")

        if message["type"] == "fake":
            self.agent.fake_message_received()

        # Propagate the message to neighbors
        if message["ttl"] > 0:
            # Create a copy of the message with decremented TTL
            relayed_message = message.copy()
            relayed_message["ttl"] -= 1
            self.send_message(relayed_message)
        else:
            print(f"[🛑 {self.agent.get_id()}] TTL expired for {msg_id[:6]}")


    
    
    def create_message(self, content: str, msg_type: str = "info") -> dict:
        msg_id = str(uuid.uuid4())
        self.seen_message_ids.add(msg_id)

        message_type_ttl = {
            "info": 3,
            "bsm": 1,
            "demn": 5,
            "fake": 4
        }
        ttl = message_type_ttl.get(msg_type.lower(), 2)

        return {
            "id": msg_id,
            "sender_id": self.agent.get_id(),
            "type": msg_type,
            "content": content,
            "position": self.agent.get_position(),
            "timestamp": self.model.step_count,  
            "ttl": ttl
        }
    
    def get_reachable_neighbors(self) -> list:
        neighbors = []
        for agent in self.model.schedule.agents:  
            if (
                isinstance(agent, VANETAgent) and agent.get_id() != self.agent.get_id()):
                dist = get_distance(self.agent.get_position(), agent.get_position()) 
                if dist <= self.model.communication_range: 
                    neighbors.append(agent)
        return neighbors