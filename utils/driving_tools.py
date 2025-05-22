from typing import List, Optional, Tuple
import networkx as nx
from shapely import LineString, Point

def get_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return (dx ** 2 + dy ** 2) ** 0.5

def find_closest_edge(graph: nx.Graph, point: Tuple[float, float], max_dist: float = 0.0002) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        point_geom = Point(point)
        closest_edge = None
        min_dist = float("inf")

        for u, v in graph.edges:
            line = LineString([u, v])
            dist = point_geom.distance(line)
            if dist < min_dist and dist <= max_dist:
                min_dist = dist
                closest_edge = (u, v)

        return closest_edge