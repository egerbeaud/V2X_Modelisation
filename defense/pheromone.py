def update_pheromone(agent,message: dict):
    message["pheromone"] += 1
    print(f"[🐜 PHEROMONE] {message['id'][:6]} increased to {message['pheromone']} by {agent.get_id()}")


def has_strong_pheromone(agent,message: dict, threshold: int = 2) -> bool:
    current = message.get("pheromone", 1)
    if current < threshold:
        print(f"[🧪 PHEROMONE] Agent {agent.get_id()} considers message {message['id'][:6]} not credible yet (pheromone={current})")
        return False
    return True