def apply_reputation_policy(sender, sanity_ok: bool, receiver):

    if not sanity_ok:
        if receiver.__class__.__name__ == "RSUAgent":
            sender.reputation = max(0.0, sender.reputation - 0.1)
            print(f"[👇 GLOBAL REP - SANITY] {sender.get_id()} → {sender.reputation:.2f}")
            return
        else :
            update_local_reputation_of_agent(sender.get_id(),receiver, -0.1)
            local_reputation = get_local_reputation_of_agent(receiver, sender.get_id())
            print(f"[👇 LOCAL REP - SANITY] {sender.get_id()} → {local_reputation:.2f}")


    else :
        if receiver.__class__.__name__ == "RSUAgent":
            sender.reputation = min(1.0, sender.reputation + 0.05)
            print(f"[🌟 GLOBAL REP - SANITY +] {sender.get_id()} → {sender.reputation:.2f}")
        else:
            update_local_reputation_of_agent(sender.get_id(),receiver, 0.05)
            print(f"[🌟 LOCAL REP - SANITY +] {receiver.get_id()} sees {sender.get_id()} → {receiver.local_reputation[sender.get_id()]:.2f}")


def check_reputation(receiver, sender):
    global_reputation = sender.get_reputation()

    if receiver.__class__.__name__ == "RSUAgent":
        if global_reputation <= 0.2:
            print(f"[👎 Global Reputation] {receiver.get_id()} ignore message from low-reputation agent {sender.get_id()}")
            return False
    else:
        local_reputation = get_local_reputation_of_agent(receiver, sender.get_id())
        reputation_used_by_car = (global_reputation + local_reputation) /2
        if reputation_used_by_car < 0.5:
            print(f"[👎 Local Reputation] {receiver.get_id()} ignore message from low-reputation agent {sender.get_id()}")
            return False
    return True


def get_local_reputation_of_agent(receiver, sender_id):
    return receiver.local_reputation.get(sender_id, 1.0)

def update_local_reputation_of_agent(sender_id: int, receiver, reputation: float):
    if sender_id not in receiver.local_reputation:
        receiver.local_reputation[sender_id] = min(1.0 , 1.0 +reputation)
    else:
        receiver.local_reputation[sender_id] = min(1.0, max(receiver.local_reputation[sender_id] + reputation, 0.0))
