"""
Graph visualization using matplotlib and networkx
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional
import os

class GraphVisualizer:
    """Class for visualizing graphs and routes"""
    
    def __init__(self, graph):
        """
        Initialize visualizer
        
        Args:
            graph: Graph object from graph.py
        """
        self.graph = graph
        self.nx_graph = None
        self._convert_to_networkx()
    
    def _convert_to_networkx(self):
        """Convert custom graph to NetworkX graph for visualization"""
        self.nx_graph = nx.DiGraph()
        
        # Add nodes with positions
        for node, (lat, lon) in self.graph.node_coordinates.items():
            self.nx_graph.add_node(node, pos=(lon, lat))
        
        # Add edges
        for source, neighbors in self.graph.adjacency_list.items():
            for neighbor, distance, time, road_type, toll in neighbors:
                self.nx_graph.add_edge(source, neighbor, 
                                       weight=distance, 
                                       time=time,
                                       road_type=road_type,
                                       toll=toll)
    
    def draw_graph(self, title: str = "Route Network Graph", 
                   show_labels: bool = True, 
                   figsize: tuple = (12, 8),
                   save_path: Optional[str] = None):
        """
        Draw the complete graph
        
        Args:
            title: Graph title
            show_labels: Whether to show node labels
            figsize: Figure size (width, height)
            save_path: Path to save the figure (optional)
        """
        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)
        os.makedirs('images', exist_ok=True)
        
        plt.figure(figsize=figsize)
        
        # Get node positions
        pos = nx.get_node_attributes(self.nx_graph, 'pos')
        
        # Draw nodes
        nx.draw_networkx_nodes(self.nx_graph, pos, node_color='lightblue', 
                               node_size=500, node_shape='o')
        
        # Draw edges
        nx.draw_networkx_edges(self.nx_graph, pos, edge_color='gray', 
                               arrows=True, arrowsize=20, width=1.5)
        
        # Draw labels
        if show_labels:
            nx.draw_networkx_labels(self.nx_graph, pos, font_size=10, font_weight='bold')
        
        # Draw edge labels (distances)
        edge_labels = {(u, v): f"{d['weight']}km" for u, v, d in self.nx_graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels, font_size=8)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Graph saved to {save_path}")
        else:
            # Default save path
            default_path = "outputs/graph_visualization.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            print(f"✓ Graph saved to {default_path}")
        
        plt.show()
        plt.close()
    
    def draw_route(self, path: List[str], title: str = "Optimal Route", 
                   figsize: tuple = (12, 8), save_path: Optional[str] = None):
        """
        Draw a specific route on the graph
        
        Args:
            path: List of nodes in the route
            title: Graph title
            figsize: Figure size
            save_path: Path to save the figure
        """
        # Create directories
        os.makedirs('outputs', exist_ok=True)
        os.makedirs('images', exist_ok=True)
        
        plt.figure(figsize=figsize)
        
        # Get node positions
        pos = nx.get_node_attributes(self.nx_graph, 'pos')
        
        # Draw all nodes
        nx.draw_networkx_nodes(self.nx_graph, pos, node_color='lightgray', 
                               node_size=400, node_shape='o')
        
        # Draw all edges
        nx.draw_networkx_edges(self.nx_graph, pos, edge_color='lightgray', 
                               arrows=True, arrowsize=15, width=1)
        
        # Highlight route edges
        route_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(self.nx_graph, pos, edgelist=route_edges, 
                               edge_color='red', width=3, arrows=True, arrowsize=20)
        
        # Highlight route nodes
        nx.draw_networkx_nodes(self.nx_graph, pos, nodelist=path, 
                               node_color='red', node_size=600)
        
        # Draw start and end nodes differently
        if path:
            nx.draw_networkx_nodes(self.nx_graph, pos, nodelist=[path[0]], 
                                   node_color='green', node_size=700, node_shape='s')
            nx.draw_networkx_nodes(self.nx_graph, pos, nodelist=[path[-1]], 
                                   node_color='blue', node_size=700, node_shape='*')
        
        # Draw labels
        nx.draw_networkx_labels(self.nx_graph, pos, font_size=10, font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', edgecolor='black', label='Start'),
            Patch(facecolor='blue', edgecolor='black', label='Destination'),
            Patch(facecolor='red', edgecolor='black', label='Route'),
            Patch(facecolor='lightgray', edgecolor='black', label='Other Nodes')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Route visualization saved to {save_path}")
        else:
            default_path = f"outputs/route_visualization.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            print(f"✓ Route visualization saved to {default_path}")
        
        plt.show()
        plt.close()
    
    def draw_comparison(self, routes: dict, title: str = "Route Comparison", 
                        figsize: tuple = (14, 10), save_path: Optional[str] = None):
        """
        Draw multiple routes for comparison
        
        Args:
            routes: Dictionary with route names as keys and paths as values
            title: Graph title
            figsize: Figure size
            save_path: Path to save the figure
        """
        # Create directories
        os.makedirs('outputs', exist_ok=True)
        
        plt.figure(figsize=figsize)
        
        pos = nx.get_node_attributes(self.nx_graph, 'pos')
        
        # Draw base graph
        nx.draw_networkx_nodes(self.nx_graph, pos, node_color='lightgray', 
                               node_size=400, node_shape='o')
        nx.draw_networkx_edges(self.nx_graph, pos, edge_color='lightgray', 
                               arrows=True, arrowsize=15, width=1)
        
        # Color map for different routes
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for idx, (name, path) in enumerate(routes.items()):
            if path:
                route_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                color = colors[idx % len(colors)]
                nx.draw_networkx_edges(self.nx_graph, pos, edgelist=route_edges, 
                                       edge_color=color, width=2.5, arrows=True, 
                                       arrowsize=15, label=name, alpha=0.7)
        
        # Draw labels
        nx.draw_networkx_labels(self.nx_graph, pos, font_size=9, font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.legend(loc='upper right')
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison saved to {save_path}")
        else:
            default_path = "outputs/route_comparison.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison saved to {default_path}")
        
        plt.show()
        plt.close()
    
    def save_graph_stats_image(self, stats: dict, save_path: str = "outputs/graph_stats.png"):
        """
        Create and save a statistics visualization
        
        Args:
            stats: Dictionary with graph statistics
            save_path: Path to save the figure
        """
        # Create outputs directory
        os.makedirs('outputs', exist_ok=True)
        
        plt.figure(figsize=(10, 6))
        
        # Create bar chart for statistics
        categories = ['Nodes', 'Edges']
        values = [stats['num_nodes'], stats['num_edges']]
        
        plt.bar(categories, values, color=['lightblue', 'lightgreen'])
        plt.title('Graph Statistics', fontsize=14, fontweight='bold')
        plt.ylabel('Count')
        
        # Add value labels on bars
        for i, v in enumerate(values):
            plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Statistics saved to {save_path}")
        plt.close()