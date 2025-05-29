def apply_reputation_policy(sender, sanity_ok: bool):
    if not hasattr(sender, "reputation"):
        return

    if not sanity_ok:
        sender.reputation = max(0.0, sender.reputation - 0.1)
        print(f"[👇 REPUTATION - SANITY] {sender.get_id()} → {sender.reputation:.2f}")
        return
    else : 
        sender.reputation = min(1.0, sender.reputation + 0.05)
        print(f"[🌟 REPUTATION +] {sender.get_id()} → {sender.reputation:.2f}")


def check_reputation(agent, sender):
    if hasattr(sender, "reputation"):
            if sender.reputation < 0.2:
                print(f"[👎 Reputation] {agent.get_id()} ignore message from low-reputation agent {sender.get_id()}")
                return False
    return True