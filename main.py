"""
Intelligent Route Planner - Main Entry Point
A complete route planning system using graph algorithms
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.graph import Graph
from src.algorithms import GraphAlgorithms
from src.route_planner import RoutePlanner
from src.utils import (
    validate_location, get_all_locations, format_duration, 
    format_distance, save_route_to_file, create_sample_dataset,
    clear_screen, print_header, print_footer
)

# Optional imports for visualization
try:
    from src.visualization import GraphVisualizer
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Note: matplotlib/networkx not installed. Visualization disabled.")
    print("Install with: pip install matplotlib networkx\n")

class RoutePlannerApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.graph = None
        self.algorithms = None
        self.planner = None
        self.visualizer = None
    
    def initialize(self):
        """Initialize graph and algorithms"""
        print_header("INTELLIGENT ROUTE PLANNER")
        print("Initializing system...")
        
        # Create sample dataset if needed
        create_sample_dataset()
        
        # Load graph
        self.graph = Graph()
        try:
            self.graph.load_from_csv('data/locations.csv', 'data/roads.csv')
            print("✓ Graph loaded successfully")
            
            # Display graph statistics
            stats = self.graph.get_graph_stats()
            print(f"  - Nodes: {stats['num_nodes']}")
            print(f"  - Edges: {stats['num_edges']}")
            print(f"  - Average Degree: {stats['avg_degree']:.2f}")
            
            # Initialize algorithms and planner
            self.algorithms = GraphAlgorithms(self.graph)
            self.planner = RoutePlanner(self.graph, self.algorithms)
            
            # Initialize visualizer if available
            if VISUALIZATION_AVAILABLE:
                self.visualizer = GraphVisualizer(self.graph)
                print("✓ Visualization module loaded")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading graph: {e}")
            return False
    
    def display_menu(self):
        """Display main menu"""
        print_header("MAIN MENU")
        print("1. Find Shortest Path (Distance)")
        print("2. Find Fastest Path (Time)")
        print("3. Find Cheapest Path (Cost)")
        print("4. Compare Different Routes")
        print("5. Show All Available Locations")
        print("6. Show Adjacency List")
        print("7. Run BFS/DFS Traversal")
        print("8. Visualize Graph (if available)")
        print("9. Compare Algorithms (BFS vs DFS vs Dijkstra)")
        print("0. Exit")
        print("-" * 70)
    
    def find_route(self, optimization: str):
        """
        Find and display route based on optimization
        
        Args:
            optimization: "distance", "time", or "cost"
        """
        clear_screen()
        print_header(f"FIND OPTIMAL ROUTE - {optimization.upper()}")
        
        # Show available locations
        locations = get_all_locations(self.graph)
        print(f"Available locations: {', '.join(sorted(locations))}")
        print("-" * 70)
        
        # Get source
        while True:
            source = input(f"\nEnter source location: ").strip().upper()
            if validate_location(source, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Get destination
        while True:
            destination = input(f"Enter destination location: ").strip().upper()
            if validate_location(destination, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Find route
        print("\n🔄 Finding optimal route...")
        path, stats = self.planner.find_route(source, destination, optimization)
        
        if path:
            # Display results
            print("\n" + "="*70)
            print("✓ OPTIMAL ROUTE FOUND!")
            print("="*70)
            print(f"\nRoute: {' → '.join(path)}")
            print(f"\nStatistics:")
            
            if optimization == "distance":
                print(f"  Total Distance: {format_distance(stats['actual_distance_km'])}")
                print(f"  Estimated Time: {format_duration(stats['actual_time_minutes'])}")
            elif optimization == "time":
                print(f"  Total Time: {format_duration(stats['actual_time_minutes'])}")
                print(f"  Total Distance: {format_distance(stats['actual_distance_km'])}")
            else:
                print(f"  Total Cost: {stats['total_cost']} points")
                print(f"  Actual Time: {format_duration(stats['actual_time_minutes'])}")
                print(f"  Distance: {format_distance(stats['actual_distance_km'])}")
            
            print(f"  Toll Roads: {stats['total_tolls']}")
            
            # Option to save
            save = input("\nSave route summary to file? (y/n): ").strip().lower()
            if save == 'y':
                summary = self.planner.generate_route_summary(source, destination, optimization)
                save_route_to_file(summary)
            
            # Option to visualize
            if VISUALIZATION_AVAILABLE and self.visualizer:
                vis = input("Visualize route on graph? (y/n): ").strip().lower()
                if vis == 'y':
                    self.visualizer.draw_route(path, title=f"Optimal Route - {optimization.upper()}")
        
        else:
            print(f"\n✗ No route found from {source} to {destination}")
        
        input("\nPress Enter to continue...")
    
    def compare_routes(self):
        """Compare different optimization strategies"""
        clear_screen()
        print_header("COMPARE DIFFERENT ROUTES")
        
        # Show available locations
        locations = get_all_locations(self.graph)
        print(f"Available locations: {', '.join(sorted(locations))}")
        print("-" * 70)
        
        # Get source
        while True:
            source = input(f"\nEnter source location: ").strip().upper()
            if validate_location(source, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Get destination
        while True:
            destination = input(f"Enter destination location: ").strip().upper()
            if validate_location(destination, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Compare routes
        self.planner.compare_routes(source, destination)
        
        # Option to visualize comparison
        if VISUALIZATION_AVAILABLE and self.visualizer:
            vis = input("\nVisualize route comparison? (y/n): ").strip().lower()
            if vis == 'y':
                routes = {}
                for opt in ["distance", "time", "cost"]:
                    path, _ = self.planner.find_route(source, destination, opt)
                    if path:
                        routes[opt.capitalize()] = path
                if routes:
                    self.visualizer.draw_comparison(routes, title="Route Comparison")
        
        input("\nPress Enter to continue...")
    
    def show_locations(self):
        """Show all available locations"""
        clear_screen()
        print_header("AVAILABLE LOCATIONS")
        
        locations = get_all_locations(self.graph)
        print("\nAll locations in the route network:")
        for i, loc in enumerate(sorted(locations), 1):
            coords = self.graph.node_coordinates.get(loc, (0, 0))
            print(f"  {i}. {loc} (lat: {coords[0]}, lon: {coords[1]})")
        
        print(f"\nTotal locations: {len(locations)}")
        input("\nPress Enter to continue...")
    
    def show_adjacency_list(self):
        """Display adjacency list"""
        clear_screen()
        self.graph.display_adjacency_list()
        input("\nPress Enter to continue...")
    
    def run_traversal(self):
        """Run BFS and DFS traversal"""
        clear_screen()
        print_header("GRAPH TRAVERSAL (BFS/DFS)")
        
        locations = get_all_locations(self.graph)
        print(f"Available locations: {', '.join(sorted(locations))}")
        print("-" * 70)
        
        # Get start node
        while True:
            start = input(f"\nEnter start location: ").strip().upper()
            if validate_location(start, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Get end node
        while True:
            end = input(f"Enter destination location: ").strip().upper()
            if validate_location(end, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        print(f"\n🔄 Running traversals from {start} to {end}...")
        
        # BFS
        bfs_path = self.algorithms.bfs(start, end)
        print(f"\n📊 BFS Path: {bfs_path}")
        print(f"   Length: {len(bfs_path) if bfs_path else 0} nodes")
        
        # DFS
        dfs_path = self.algorithms.dfs(start, end)
        print(f"\n📊 DFS Path: {dfs_path}")
        print(f"   Length: {len(dfs_path) if dfs_path else 0} nodes")
        
        # Dijkstra (for comparison)
        dijkstra_path, _ = self.algorithms.dijkstra(start, end, "time")
        print(f"\n📊 Dijkstra (Fastest): {dijkstra_path}")
        
        input("\nPress Enter to continue...")
    
    def compare_algorithms(self):
        """Compare BFS, DFS, and Dijkstra"""
        clear_screen()
        print_header("ALGORITHM COMPARISON")
        
        locations = get_all_locations(self.graph)
        print(f"Available locations: {', '.join(sorted(locations))}")
        print("-" * 70)
        
        # Get source and destination
        while True:
            source = input(f"\nEnter source location: ").strip().upper()
            if validate_location(source, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        while True:
            destination = input(f"Enter destination location: ").strip().upper()
            if validate_location(destination, self.graph):
                break
            print(f"✗ Invalid location. Available: {', '.join(sorted(locations))}")
        
        # Compare
        self.algorithms.compare_algorithms(source, destination)
        input("\nPress Enter to continue...")
    
    def visualize_graph(self):
        """Visualize the graph"""
        if not VISUALIZATION_AVAILABLE or not self.visualizer:
            print("\n✗ Visualization not available. Install matplotlib and networkx")
            print("  Run: pip install matplotlib networkx")
            input("\nPress Enter to continue...")
            return
        
        clear_screen()
        print_header("GRAPH VISUALIZATION")
        
        print("\n1. Show Complete Graph")
        print("2. Show Graph Statistics")
        print("3. Run Sample Route Visualization")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            self.visualizer.draw_graph(title="Complete Route Network")
        elif choice == '2':
            stats = self.graph.get_graph_stats()
            self.visualizer.save_graph_stats_image(stats)
            print("\n✓ Statistics image saved to 'outputs/graph_stats.png'")
        elif choice == '3':
            # Run a sample route
            locations = get_all_locations(self.graph)
            if len(locations) >= 2:
                path, _ = self.planner.find_route(locations[0], locations[-1], "time")
                if path:
                    self.visualizer.draw_route(path, title="Sample Optimal Route")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            print("Failed to initialize. Exiting...")
            return
        
        while True:
            clear_screen()
            self.display_menu()
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.find_route("distance")
            elif choice == '2':
                self.find_route("time")
            elif choice == '3':
                self.find_route("cost")
            elif choice == '4':
                self.compare_routes()
            elif choice == '5':
                self.show_locations()
            elif choice == '6':
                self.show_adjacency_list()
            elif choice == '7':
                self.run_traversal()
            elif choice == '8':
                self.visualize_graph()
            elif choice == '9':
                self.compare_algorithms()
            elif choice == '0':
                print_header("GOODBYE!")
                print("Thank you for using Intelligent Route Planner!\n")
                break
            else:
                print("\n✗ Invalid choice. Please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = RoutePlannerApp()
    app.run()