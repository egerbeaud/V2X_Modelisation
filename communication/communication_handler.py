import random
from typing import List
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import TrafficSimulationModel

from interfaces.vanetAgent import VANETAgent

from utils.driving_tools import get_distance

from defense.sanity import *
from defense.reputation import *
from defense.pheromone import *



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

        # Update the list of neighbours
        self.current_neighbors = self.get_reachable_neighbors()


        # for agent in self.current_neighbors:
        #     print(f"[📥 CAM received by {agent.get_id()}] from {self.agent.get_id()} → Pos={cam['position']} V={cam['speed']:.2f}") 



    def send_message(self, message: dict):
        msg_id = message["id"]
        if message["ttl"] <= 0:
            return        

        print(f"{self.format_agent_label(self.agent)} Send the message {msg_id[:6]} (TTL={message['ttl']}) : \"{message['content']}\"")


        forwarded = False

        for agent in self.current_neighbors:
            if agent.get_id() == self.agent.get_id():
                continue
            if msg_id in agent.communicationHandler.seen_message_ids:
                continue

            
            if agent.receive_message(message): 
                print(f"    ↳ Forwarded to {self.format_agent_label(agent)} the message from {message['sender_id']}")
                forwarded = True
        
        if not self.current_neighbors or not forwarded:
            print(f"{self.format_agent_label(self.agent)} (no neighbours nearby)")



    def receive_message(self, message: dict):
        msg_id = message["id"]

        if msg_id in self.seen_message_ids:
            return False
        
        self.seen_message_ids.add(msg_id)
        self.received_messages.append(message)
        self.last_message = message["content"]

        
        # Recup the sender agent
        sender = self.get_agent_from_id(message["sender_id"])

        print(f"[📨 {self.agent.get_id()}] Received {msg_id[:6]} from {message['sender_id']} : {message['content']}")

        if not check_reputation(self.agent,sender):
            return False
        

        sanity = True
        if message["sender_id"] != self.agent.get_id():
            if not sanity_check(self,message):
                sanity = False
                print(f"[🚫 SanityCheck] {self.agent.get_id()} ignored message {msg_id[:6]} : {message['content']}")
                apply_reputation_policy(sender, sanity)
                return False
            
            update_pheromone(self.agent,message)

            if not has_strong_pheromone(self.agent,message):
                return False

            apply_reputation_policy(sender, sanity)
        
        if message.get("is_fake", False):
            self.agent.fake_message_received()


        # Propagate the message to neighbors
        if message["ttl"] > 0:
            # Create a copy of the message with decremented TTL
            relayed_message = message.copy()
            relayed_message["ttl"] -= 1
            self.send_message(relayed_message)
            return True
        else:
            print(f"[🛑 {self.agent.get_id()}] TTL expired for {msg_id[:6]}")
            return False



    def create_message(self, content: str, msg_type: str = "info", is_fake : bool = False) -> dict:
        msg_id = str(uuid.uuid4())
        self.seen_message_ids.add(msg_id)

        message_type_ttl = {
            "info": 3,
            "bsm": 1,
            "demn": 5,
        }
        ttl = message_type_ttl.get(msg_type.lower(), 2)

        return {
            "id": msg_id,
            "sender_id": self.agent.get_id(),
            "type": msg_type,
            "content": content,
            "position": self.agent.get_position(),
            "timestamp": self.model.step_count,  
            "ttl": ttl,
            "is_fake": is_fake,
            "pheromone": 1
        }
    
    def get_reachable_neighbors(self) -> list:
        neighbors = []
        for agent in self.model.schedule.agents:  
            if agent.get_id() == self.agent.get_id():
                continue
            if (
                isinstance(agent, VANETAgent) and agent.get_id() != self.agent.get_id()):
                dist = get_distance(self.agent.get_position(), agent.get_position()) 
                range_used = getattr(self.agent, 'communication_range', self.model.communication_range)
                if dist <= range_used: 
                    neighbors.append(agent)
        return neighbors        
    

    def format_agent_label(self, agent) -> str:
        if agent.__class__.__name__ == "RSUAgent":
            return f"🛰️ {agent.get_id()}"
        return f"🚗 {agent.get_id()}"
    

    def get_agent_from_id(self, agent_id):
        for agent in self.model.schedule.agents:
            if agent.get_id() == agent_id:
                return agent
        return None

    
    




    

