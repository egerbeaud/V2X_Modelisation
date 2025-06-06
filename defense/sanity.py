import random


from utils.driving_tools import get_distance

def sanity_check(handler, message):
    agent = handler.agent
    model = handler.model

    score = 0
    total_checks = 0
    content = message["content"].lower()

    # Distance entre l'agent et la position du message
    dist = get_distance(agent.get_position(), message["position"])
    speed = agent.get_speed_kmh()
    msg_speed = message["speed"]
    time_diff = abs(model.step_count - message["timestamp"])

    # ------- CONTEXTE 1 : ACCIDENT -------
    if "accident" in content:
        total_checks += 2
        if msg_speed < 10:
            score += 1
        else:
            print(f"[Sanity ❌] Not credible (accident): speed {msg_speed} too high")
            return False

        if dist < 30:
            score += 1
        else:
            print(f"[Sanity ❌] Not credible (accident): agent too far ({dist:.1f}m)")

    # ------- CONTEXT 2: FOG -------
    elif "fog" in content:
        total_checks += 2
        if dist < 25:
            score += 1
        else:
            print(f"[Sanity ❌] Fog reported but agent too far ({dist:.1f}m)")
            return False

        if time_diff < 5:
            score += 1
        else:
            print(f"[Sanity ❌] Fog too old (Δt = {time_diff} steps)")

    # ------- CONTEXT 3: CONGESTION -------
    elif "congestion" in content or "slowdown" in content:
        total_checks += 2
        if msg_speed < 15:
            score += 1
        else:
            print(f"[Sanity ❌] Congestion: speed too high ({msg_speed})")
            return False

        if dist < 40:
            score += 1
        else:
            print(f"[Sanity ❌] Congestion reported but agent too far ({dist:.1f}m)")

    # ------- CONTEXT 4: RADAR -------
    elif "radar" in content:
        total_checks += 1
        if dist < 50:
            score += 1
        else:
            print(f"[Sanity ❌] Radar reported too far ({dist:.1f}m)")

    # ------- GENERIC CONTEXT -------
    else:
        total_checks += 2
        if abs(speed - msg_speed) < 15:
            score += 1
        else:
            print(f"[Sanity ❌] Suspicious speed difference: {speed} vs {msg_speed}")

        if time_diff <= 5:
            score += 1
        else:
            print(f"[Sanity ❌] Message too old (Δt = {time_diff} steps)")

    # ------- Summary -------
    result = score >= max(1, total_checks - 1)
    print(f"[Sanity 🧠] Score {score}/{total_checks} → {'PASS ✅' if result else 'REJECT ❌'}")

    return result
