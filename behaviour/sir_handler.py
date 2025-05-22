from enum import Enum

class SirState(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"


class SirHandler:
    def __init__(self, agent_id : int, recovery_time: int = 30):
        self.agent_id = agent_id
        self.state = SirState.SUSCEPTIBLE
        self.infection_timer = 0
        self.recovery_time = recovery_time

    def infect(self):
        if self.state == SirState.SUSCEPTIBLE:
            self.state = SirState.INFECTED
            self.infection_timer = 0
            print(f"[🦠 {self.agent_id}] infected !")

            return True
        return False

    def recover(self):
        if self.state == SirState.INFECTED:
            self.state = SirState.RECOVERED
            print(f"[💊 {self.agent_id}] healed !")


    def update(self):
        if self.state == SirState.INFECTED:
            self.infection_timer += 1
            if self.infection_timer >= self.recovery_time:
                self.recover()

