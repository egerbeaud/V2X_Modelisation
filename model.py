# model.py
from mesa import Model
from mesa.time import SimultaneousActivation
from agents.rsu import RSUAgent
from agents.unconnected_car_agent import UnconnectedCarAgent
from agents.connected_car_agent import ConnectedCarAgent
from agents.traffic_light_agent import TrafficLightAgent
from agents.attacker_car_agent import AttackerCarAgent
import random
import networkx as nx
from utils.map_loader import load_road_graph
from typing import List, Tuple, cast
import geopandas as gpd
from utils.driving_tools import find_closest_edge


class TrafficSimulationModel(Model):
    def __init__(self, shapefile_path, num_connected_cars=3, num_unconnected_cars=3, num_attacker_cars=3):
        super().__init__()

        # Load the road graph (shapefile → graph)
        self.road_graph = load_road_graph(shapefile_path)

        # Load shapefiles of roads and buildings
        self.roads = gpd.read_file(shapefile_path)
        self.buildings = gpd.read_file("buildings/building.shp")
        self.traffic_lights = gpd.read_file("infrastructures/traffic_lights.geojson")

        # Planificateur (gère les agents et le temps)
        self.schedule = SimultaneousActivation(self)
        self.step_count = 0

        #Communication
        self.communication_range = 0.0002

        self.num_connected_cars = num_connected_cars
        self.num_unconnected_cars = num_unconnected_cars

        self.message_accepted = 0
        self.message_rejected = 0

        self.defense_stats = {
        "sanity": 0,
        "reputation": 0,
        "pheromone": 0
        }


        # Creating RSUs
        rsu1 = RSUAgent(unique_id=1000, model=self, position=(23.803283, 44.319399), communication_range=0.0015)
        self.schedule.add(rsu1)
        rsu2 = RSUAgent(unique_id=1001, model=self, position=(23.802103, 44.318800), communication_range=0.0012)
        self.schedule.add(rsu2)

        # Creating connected cars
        nodes = list(self.road_graph.nodes)
        created_cars = 0
        id = 0
        while created_cars < num_connected_cars:
            start = random.choice(nodes)
            end = random.choice(nodes)
            if start == end:
                continue

            try:
                id += 1
                path = cast(List[Tuple[float, float]], nx.shortest_path(
                    self.road_graph,
                    source=start,
                    target=end,
                    weight="weight"
                ))
                connected_car = ConnectedCarAgent(
                    unique_id=id, model=self, path=path)
                self.schedule.add(connected_car)
                created_cars += 1
            except nx.NetworkXNoPath:
                continue
        
        # Creating unconnected cars
        created_cars = 0
        while created_cars < num_unconnected_cars:
            start = random.choice(nodes)
            end = random.choice(nodes)
            if start == end:
                continue

            try:
                id += 1
                path = cast(List[Tuple[float, float]], nx.shortest_path(
                    self.road_graph,
                    source=start,
                    target=end,
                    weight="weight"
                ))
                unconnected_car = UnconnectedCarAgent(
                    unique_id=id, model=self, path=path)
                self.schedule.add(unconnected_car)
                created_cars += 1
            except nx.NetworkXNoPath:
                continue


        # Creating attacker cars
        created_cars = 0
        while created_cars < num_attacker_cars:
            start = random.choice(nodes)
            end = random.choice(nodes)
            if start == end:
                continue

            try:
                id += 1
                path = cast(List[Tuple[float, float]], nx.shortest_path(
                    self.road_graph,
                    source=start,
                    target=end,
                    weight="weight"
                ))
                attacker_car = AttackerCarAgent(
                    unique_id=id, model=self, path=path)
                self.schedule.add(attacker_car)
                created_cars += 1
            except nx.NetworkXNoPath:
                continue
    
        # Creating traffic lights
        for i, row in self.traffic_lights.iterrows():
            id += 1
            x, y = row.geometry.x, row.geometry.y
            pos = (x, y)
            controlled_edge = find_closest_edge(self.road_graph, pos)

            if controlled_edge:
                traffic_light = TrafficLightAgent(
                    unique_id=id,
                    model=self,
                    position=pos,
                    state=random.choice(["red", "green"])
                )
                traffic_light.controlled_edges = [controlled_edge]
                self.schedule.add(traffic_light)




        
    


    def step(self):
        """Fait avancer tous les agents"""
        self.step_count += 1
        self.schedule.step()

    

