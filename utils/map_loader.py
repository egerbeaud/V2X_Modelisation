import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString

def load_road_graph(shapefile_path: str) -> nx.DiGraph:
    gdf = gpd.read_file(shapefile_path)
    G = nx.DiGraph()

    for _, row in gdf.iterrows():
        geom = row.geometry
        if isinstance(geom, LineString):
            coords = list(geom.coords)

            maxspeed = row.get("maxspeed", None)
            highway_type = row.get("highway", "unknown")
            lanes = row.get("lanes", None)
            is_oneway = row.get("oneway") == "yes"

            for u, v in zip(coords[:-1], coords[1:]):
                dist = ((u[0] - v[0])**2 + (u[1] - v[1])**2)**0.5

                attrs = {
                    "weight": dist,
                    "maxspeed": maxspeed,
                    "highway": highway_type,
                    "lanes": lanes,
                }

                if is_oneway:
                    G.add_edge(u, v, **attrs)
                else:
                    G.add_edge(u, v, **attrs)
                    G.add_edge(v, u, **attrs)

    return G