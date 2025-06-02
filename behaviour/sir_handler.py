from enum import Enum

class SirState(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"


class SirHandler:
    def __init__(self, agent_id : int, recovery_time: int = 20, immunity_duration: int = 20):
        self.agent_id = agent_id
        self.state = SirState.SUSCEPTIBLE
        self.infection_timer = 0
        self.recovery_time = recovery_time
        self.immunity_duration = immunity_duration

    def infect(self):
        if self.state == SirState.SUSCEPTIBLE:
            self.state = SirState.INFECTED
            self.infection_timer = 0
            print(f"[🦠 {self.agent_id}] infected !")

            return True
        return False

    def recover(self):
        if self.state == SirState.INFECTED:
            self.state = SirState.SUSCEPTIBLE
            self.infection_timer = 0
            print(f"[💊 {self.agent_id}] healed ! It's now suspectible again !")


    def update(self):
        if self.state == SirState.INFECTED:
            self.infection_timer += 1
            if self.infection_timer >= self.recovery_time:
                self.recover()
        elif self.state == SirState.RECOVERED:
            self.immunity_timer += 1
            if self.immunity_timer >= self.immunity_duration:
                self.state = SirState.SUSCEPTIBLE
                print(f"[🔁 {self.agent_id}] defense expired, now susceptible again.")



    def defend_successfully(self):
        if self.state == SirState.SUSCEPTIBLE:
            self.state = SirState.RECOVERED
            self.immunity_timer = 0
            print(f"[🛡️ {self.agent_id}] defended and became temporarily immune!")

    def get_state(self) -> SirState:
        return self.state

