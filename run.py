# run.py
import matplotlib.pyplot as plt
from behaviour.sir_handler import SirState
from model import TrafficSimulationModel
from agents.unconnected_car_agent import UnconnectedCarAgent
from agents.connected_car_agent import ConnectedCarAgent as connected_car_agent
from agents.traffic_light_agent import TrafficLightAgent as traffic_light_agent
from matplotlib.lines import Line2D
from agents.rsu import RSUAgent


# Initialise the model
model = TrafficSimulationModel(shapefile_path="roads/routes.shp", num_conneted_cars=30, num_unconnected_cars=5)

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

        # Connected car
        if isinstance(agent, connected_car_agent):
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
        elif isinstance(agent, traffic_light_agent):
            color = "red" if agent.is_red() else "green"
            ax.plot(x, y, 's', color=color, markersize=5)
        
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
        if isinstance(a, connected_car_agent):
            if a.sir.state == SirState.SUSCEPTIBLE:
                susceptible_count += 1
            elif a.sir.state == SirState.INFECTED:
                infected_count += 1
            elif a.sir.state == SirState.RECOVERED:
                recovered_count += 1

    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=f'Connecté (S) [{susceptible_count}]', markerfacecolor='green', markersize=6),
        Line2D([0], [0], marker='o', color='w', label=f'Infecté (I) [{infected_count}]', markerfacecolor='red', markersize=6),
        Line2D([0], [0], marker='o', color='w', label=f'Guéri (R) [{recovered_count}]', markerfacecolor='blue', markersize=6),
        Line2D([0], [0], marker='*', color='w', label='RSU', markerfacecolor='purple', markersize=6),
        Line2D([0], [0], marker='o', color='w', label='Non connecté', markerfacecolor='saddlebrown', markersize=6),
        Line2D([0], [0], marker='s', color='w', label='Feu rouge', markerfacecolor='red', markersize=8),
        Line2D([0], [0], marker='s', color='w', label='Feu vert', markerfacecolor='green', markersize=8),
    ]

    ax.legend(handles=legend_elements, loc='upper right')

# Run the simulation
for step in range(100):
    plot_step(step)
    model.step()
    plt.pause(0.4)

plt.show()

