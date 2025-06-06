import csv
import os
from datetime import datetime

def log_simulation_results(model, infected_count, recovered_count):
    # Crée le dossier "results" s'il n'existe pas
    os.makedirs("results", exist_ok=True)

    filepath = os.path.join("results", "simulation_results.csv")
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "timestamp", "nb_connected", "nb_attackers", "nb_unconnected", "steps",
            "sanity_enabled", "reputation_enabled", "pheromone_enabled",
            "messages_sent", "messages_accepted", "messages_rejected", "messages_forwarded_without_believing",
            "rejected_by_sanity", "rejected_by_reputation", "rejected_by_pheromone",
            "infected", "recovered"
        ], delimiter=';')  # Important : point-virgule comme séparateur

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "nb_connected": model.nb_connected,
            "nb_attackers": model.nb_attacker,
            "nb_unconnected": model.nb_unconnected,
            "steps": model.steps,
            "sanity_enabled": model.sanity_check_enabled,
            "reputation_enabled": model.reputation_enabled,
            "pheromone_enabled": model.pheromone_enabled,
            "messages_sent": model.message_sent,
            "messages_accepted": model.message_accepted,
            "messages_rejected": model.message_rejected,
            "messages_forwarded_without_believing": model.message_forwarded_without_believing,
            "rejected_by_sanity": model.defense_stats["sanity"],
            "rejected_by_reputation": model.defense_stats["reputation"],
            "rejected_by_pheromone": model.defense_stats["pheromone"],
            "infected": infected_count,
            "recovered": recovered_count
        })

    print(f"✅ Résultats enregistrés dans : {filepath}")