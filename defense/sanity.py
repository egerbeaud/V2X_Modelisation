import random


def sanity_check(communicationHandler, message):
        neighbors = communicationHandler.get_reachable_neighbors()
        content = message["content"].lower()

        if "accident" in content:
            for n in neighbors:
                if hasattr(n, "speed") and n.speed == 0:
                    return True
            return False

        elif "road is completely free" in content or "no slowdown" in content:
            for n in neighbors:
                if hasattr(n, "speed") and n.speed <= 0:
                    return False
            return True

        elif "congestion" in content or "slowdown" in content:
            speeds = []
            for n in neighbors:
                if hasattr(n, "speed"):
                    speeds.append(n.speed)
            return len(speeds) > 2 and sum(speeds) / len(speeds) < 1.0

        elif "fog" in content or "radar" in content:
            return random.random() < 0.5  

        return True