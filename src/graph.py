"""
Graph representation using adjacency list
This file handles the creation and management of the graph structure
"""

import csv
from typing import Dict, List, Tuple, Optional

class Graph:
    """Graph class using adjacency list representation"""
    
    def __init__(self):
        """Initialize empty graph"""
        self.adjacency_list: Dict[str, List[Tuple[str, float, float, str, int]]] = {}
        self.node_coordinates: Dict[str, Tuple[float, float]] = {}
        self.num_nodes = 0
        self.num_edges = 0
    
    def add_node(self, node: str, lat: float = 0, lon: float = 0) -> None:
        """
        Add a node to the graph
        
        Args:
            node: Node identifier
            lat: Latitude coordinate
            lon: Longitude coordinate
        """
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            self.node_coordinates[node] = (lat, lon)
            self.num_nodes += 1
    
    def add_edge(self, source: str, destination: str, distance: float, 
                 time: float, road_type: str = "local", toll: int = 0) -> None:
        """
        Add a directed edge to the graph
        
        Args:
            source: Source node
            destination: Destination node
            distance: Distance in km
            time: Time in minutes
            road_type: Type of road (local, highway, etc.)
            toll: 1 if toll road, 0 otherwise
        """
        if source not in self.adjacency_list:
            self.add_node(source)
        if destination not in self.adjacency_list:
            self.add_node(destination)
        
        # Add edge with all attributes
        self.adjacency_list[source].append((destination, distance, time, road_type, toll))
        self.num_edges += 1
    
    def load_from_csv(self, nodes_file: str, edges_file: str) -> None:
        """
        Load graph data from CSV files
        
        Args:
            nodes_file: Path to nodes CSV file
            edges_file: Path to edges CSV file
        """
        # Load nodes
        with open(nodes_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_node(
                    row['location'],
                    float(row['lat']),
                    float(row['lon'])
                )
        
        # Load edges
        with open(edges_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_edge(
                    row['source'],
                    row['destination'],
                    float(row['distance']),
                    float(row['time']),
                    row['road_type'],
                    int(row['toll'])
                )
    
    def get_neighbors(self, node: str) -> List[Tuple[str, float, float, str, int]]:
        """
        Get all neighbors of a node
        
        Args:
            node: Node to get neighbors for
            
        Returns:
            List of tuples (neighbor, distance, time, road_type, toll)
        """
        return self.adjacency_list.get(node, [])
    
    def get_edge_weight(self, source: str, destination: str, weight_type: str = "distance") -> Optional[float]:
        """
        Get weight between two nodes
        
        Args:
            source: Source node
            destination: Destination node
            weight_type: Type of weight ("distance", "time", "cost")
            
        Returns:
            Weight value or None if edge doesn't exist
        """
        for neighbor, distance, time, road_type, toll in self.adjacency_list.get(source, []):
            if neighbor == destination:
                if weight_type == "distance":
                    return distance
                elif weight_type == "time":
                    return time
                elif weight_type == "cost":
                    # Cost = time + toll_penalty (toll roads cost extra time)
                    return time + (toll * 2)
        return None
    
    def display_adjacency_list(self) -> None:
        """Print the adjacency list representation of the graph"""
        print("\n" + "="*60)
        print("ADJACENCY LIST REPRESENTATION")
        print("="*60)
        for node, neighbors in self.adjacency_list.items():
            print(f"\n{node} ->", end=" ")
            for neighbor, dist, time, road, toll in neighbors:
                print(f"[{neighbor}: {dist}km, {time}min, {road}", end="")
                if toll:
                    print(f", TOLL]", end=" ")
                else:
                    print("]", end=" ")
        print("\n" + "="*60)
    
    def get_graph_stats(self) -> Dict:
        """
        Get graph statistics
        
        Returns:
            Dictionary with graph statistics
        """
        return {
            'num_nodes': self.num_nodes,
            'num_edges': self.num_edges,
            'nodes': list(self.adjacency_list.keys()),
            'avg_degree': (2 * self.num_edges) / self.num_nodes if self.num_nodes > 0 else 0
        }