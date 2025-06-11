# run.py
import matplotlib.pyplot as plt
from behaviour.sir_handler import SirState
from model import TrafficSimulationModel
from agents.unconnected_car_agent import UnconnectedCarAgent
from agents.connected_car_agent import ConnectedCarAgent
from agents.traffic_light_agent import TrafficLightAgent 
from agents.attacker_car_agent import AttackerCarAgent
from matplotlib.lines import Line2D
from agents.rsu import RSUAgent

import argparse
from utils.results_logger import log_simulation_results


parser = argparse.ArgumentParser()
parser.add_argument("--nb_connected", type=int, default=10)
parser.add_argument("--nb_attackers", type=int, default=2)
parser.add_argument("--nb_unconnected", type=int, default=5)
parser.add_argument("--steps", type=int, default=100)
parser.add_argument("--sanity", action="store_true")
parser.add_argument("--reputation", action="store_true")
parser.add_argument("--pheromone", action="store_true")
args = parser.parse_args()

model = TrafficSimulationModel(
    nb_connected=args.nb_connected,
    nb_attacker=args.nb_attackers,
    nb_unconnected=args.nb_unconnected,
    steps=args.steps,
    sanity_check_enabled=args.sanity,
    reputation_enabled=args.reputation,
    pheromone_enabled=args.pheromone,
    shapefile_path="roads/routes.shp"
)


# Drawing the canva
fig, ax = plt.subplots(figsize=(10, 10))

def plot_step(step_num):
    ax.clear()

    # Display the roads and buildings (map)
    model.roads.plot(ax=ax, color="gray", linewidth=1)
    model.buildings.plot(ax=ax, color="lightblue", edgecolor="black", alpha=0.5)

    # Display all agents
    for agent in model.schedule.agents:
        x, y = agent.get_position()
        # Attacker car
        if isinstance(agent, AttackerCarAgent ):
            ax.plot(x, y, 'H', color="black", markersize=6)

        # Connected car
        elif isinstance(agent, ConnectedCarAgent):
            color = "green"
            if agent.sir.state == SirState.INFECTED:
                color = "red"
            elif agent.sir.state == SirState.RECOVERED:
                color = "blue"

            ax.plot(x, y, 'o', color=color, markersize=6)

        # Unconnected car
        elif isinstance(agent, UnconnectedCarAgent):
            ax.plot(x, y, 'o', color="saddlebrown", markersize=6)


        # Traffic light
        elif isinstance(agent, TrafficLightAgent):
            color = "red" if agent.is_red() else "green"
            ax.plot(x, y, 'd', color=color, markersize=5)
        
        # RSU
        if isinstance(agent, RSUAgent):
            if agent.sir.state == SirState.INFECTED:
                ax.plot(x, y, '*', color='red', markersize=8)
            elif agent.sir.state == SirState.RECOVERED:
                ax.plot(x, y, '*', color='blue', markersize=8)
            else:
                ax.plot(x, y, '*', color='green', markersize=8)



    
    ax.set_title(f"Simulation - Step {step_num}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True)

    # Count the number of connected cars in each SIR state
    susceptible_count = 0 
    infected_count = 0  
    recovered_count = 0 

    for a in model.schedule.agents:
        if isinstance(a, ConnectedCarAgent) and not isinstance(a, AttackerCarAgent):
            if a.sir.state == SirState.SUSCEPTIBLE:
                susceptible_count += 1
            elif a.sir.state == SirState.INFECTED:
                infected_count += 1
            elif a.sir.state == SirState.RECOVERED:
                recovered_count += 1

    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=f'Susceptible (S) [{susceptible_count} / {model.nb_connected}]', markerfacecolor='green', markersize=6),
        Line2D([0], [0], marker='o', color='w', label=f'Infected (I) [{infected_count} / {model.nb_connected}]', markerfacecolor='red', markersize=6),
        Line2D([0], [0], marker='o', color='w', label=f'Recovered (R) [{recovered_count} / {model.nb_connected}]', markerfacecolor='blue', markersize=6),
        Line2D([0], [0], marker='*', color='w', label='RSU', markerfacecolor='green', markersize=8),
        Line2D([0], [0], marker='o', color='w', label=f'Unconnected ({model.nb_unconnected})', markerfacecolor='saddlebrown', markersize=6),
        Line2D([0], [0], marker='H', color='w', label=f'Attackers ({model.nb_attacker})', markerfacecolor='black', markersize=7),
        Line2D([0], [0], marker='d', color='w', label=f'Traffic lights (red / green)', markerfacecolor='gray', markersize=8),
        Line2D([0], [0], marker='', color='w', label=f"✔ Accepted : {model.message_accepted}"),
        Line2D([0], [0], marker='', color='w', label=f"✘ Refused : {model.message_rejected}"),
        Line2D([0], [0], marker='', color='w', label=f"Forwarded without believing : {model.message_forwarded_without_believing}"),
        Line2D([0], [0], marker='', color='w', label=f" Sent : {model.message_sent}"),
        Line2D([0], [0], marker='', color='w', label=f'Effective defences :'),
        Line2D([0], [0], marker='', color='w', label=f'↳ Sanity : {model.defense_stats["sanity"]}'),
        Line2D([0], [0], marker='', color='w', label=f'↳ Reputation : {model.defense_stats["reputation"]}'),
        Line2D([0], [0], marker='', color='w', label=f'↳ Pheromone : {model.defense_stats["pheromone"]}'),
    ]

    ax.legend(handles=legend_elements, loc='upper left')


if __name__ == "__main__":

    # Run the simulation
    print("Starting simulation...")
    for step in range(model.steps):
        plot_step(step)
        model.step()
        plt.pause(0.4)

    plt.show()

    infected_count = 0
    recovered_count = 0
    
    for a in model.schedule.agents:
        if isinstance(a, ConnectedCarAgent) and not isinstance(a, AttackerCarAgent):
            if a.sir.state == SirState.INFECTED:
                infected_count += 1
            elif a.sir.state == SirState.RECOVERED:
                recovered_count += 1

    log_simulation_results(model, infected_count, recovered_count)



