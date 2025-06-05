from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

from model import TrafficSimulationModel  # Assure-toi que ce fichier contient le bon constructeur avec les bons arguments
from display import agent_portrayal  # Assure-toi que ce fichier contient la fonction agent_portrayal
# --- Grille d'affichage ---
GRID_WIDTH = 30
GRID_HEIGHT = 30
CELL_SIZE = 15

grid = CanvasGrid(agent_portrayal, GRID_WIDTH, GRID_HEIGHT, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)

# --- Paramètres personnalisables ---
params = {
    "nb_connected": UserSettableParameter("slider", "Voitures connectées", 30, 0, 100, 1),
    "nb_attackers": UserSettableParameter("slider", "Voitures attaquantes", 5, 0, 50, 1),
    "nb_unconnected": UserSettableParameter("slider", "Voitures non connectées", 5, 0, 50, 1),

    "sanity_check_enabled": UserSettableParameter("checkbox", "Activer Sanity", True),
    "reputation_enabled": UserSettableParameter("checkbox", "Activer Réputation", True),
    "pheromone_enabled": UserSettableParameter("checkbox", "Activer Phéromone", True),

    "steps": UserSettableParameter("slider", "Nombre de steps (max)", 1000, 50, 10000, 50),
    "communication_range": UserSettableParameter("slider", "Portée de communication (m)", 0.008, 0.006, 0.01, 0.001),
}

# --- Serveur ---
server = ModularServer(
    TrafficSimulationModel,
    [grid],
    "Simulation V2X - Fake News Defense",
    params
)

server.port = 8521  # Tu peux changer si besoin

if __name__ == "__main__":
    server.launch()
