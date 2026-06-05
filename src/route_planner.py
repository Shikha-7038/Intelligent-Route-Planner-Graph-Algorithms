"""
Route planning and path reconstruction
Handles route optimization and summary generation
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime

class RoutePlanner:
    """Main route planning class"""
    
    def __init__(self, graph, algorithms):
        """
        Initialize route planner
        
        Args:
            graph: Graph object
            algorithms: GraphAlgorithms object
        """
        self.graph = graph
        self.algorithms = algorithms
        self.current_route = None
        self.current_stats = {}
    
    def find_route(self, start: str, end: str, optimization: str = "time") -> Tuple[Optional[List[str]], Dict]:
        """
        Find optimal route based on optimization criteria
        
        Args:
            start: Starting location
            end: Destination location
            optimization: "distance", "time", or "cost"
            
        Returns:
            Tuple of (path, statistics dictionary)
        """
        if optimization == "distance":
            path, total = self.algorithms.dijkstra(start, end, "distance")
            unit = "km"
            stat_name = "total_distance"
        elif optimization == "time":
            path, total = self.algorithms.dijkstra(start, end, "time")
            unit = "minutes"
            stat_name = "total_time"
        elif optimization == "cost":
            path, total = self.algorithms.dijkstra(start, end, "cost")
            unit = "points"
            stat_name = "total_cost"
        else:
            path, total = self.algorithms.dijkstra(start, end, "time")
            unit = "minutes"
            stat_name = "total_time"
        
        if path:
            self.current_route = path
            self.current_stats = {
                stat_name: total,
                "unit": unit,
                "optimization": optimization,
                "num_stops": len(path),
                "path": " -> ".join(path)
            }
            
            # Calculate additional stats
            actual_distance = self.calculate_path_distance(path)
            actual_time = self.calculate_path_time(path)
            actual_tolls = self.calculate_path_tolls(path)
            
            self.current_stats["actual_distance_km"] = actual_distance
            self.current_stats["actual_time_minutes"] = actual_time
            self.current_stats["total_tolls"] = actual_tolls
            
            return path, self.current_stats
        
        return None, {"error": "No path found"}
    
    def calculate_path_distance(self, path: List[str]) -> float:
        """
        Calculate total distance of a path
        
        Args:
            path: List of nodes in path
            
        Returns:
            Total distance in km
        """
        total = 0.0
        for i in range(len(path) - 1):
            weight = self.graph.get_edge_weight(path[i], path[i + 1], "distance")
            if weight:
                total += weight
        return round(total, 2)
    
    def calculate_path_time(self, path: List[str]) -> float:
        """
        Calculate total time of a path
        
        Args:
            path: List of nodes in path
            
        Returns:
            Total time in minutes
        """
        total = 0.0
        for i in range(len(path) - 1):
            weight = self.graph.get_edge_weight(path[i], path[i + 1], "time")
            if weight:
                total += weight
        return round(total, 2)
    
    def calculate_path_tolls(self, path: List[str]) -> int:
        """
        Calculate number of toll roads in a path
        
        Args:
            path: List of nodes in path
            
        Returns:
            Number of toll roads
        """
        total = 0
        for i in range(len(path) - 1):
            for neighbor, _, _, _, toll in self.graph.get_neighbors(path[i]):
                if neighbor == path[i + 1]:
                    total += toll
                    break
        return total
    
    def get_road_info(self, source: str, destination: str) -> Optional[Dict]:
        """
        Get information about a road between two nodes
        
        Args:
            source: Source node
            destination: Destination node
            
        Returns:
            Dictionary with road information
        """
        for neighbor, distance, time, road_type, toll in self.graph.get_neighbors(source):
            if neighbor == destination:
                return {
                    'distance': distance,
                    'time': time,
                    'road_type': road_type,
                    'toll': bool(toll)
                }
        return None
    
    def generate_route_summary(self, start: str, end: str, optimization: str = "time") -> str:
        """
        Generate a detailed route summary
        
        Args:
            start: Starting location
            end: Destination location
            optimization: Optimization criteria
            
        Returns:
            Formatted route summary string
        """
        path, stats = self.find_route(start, end, optimization)
        
        if not path:
            return f"\n[ERROR] No route found from {start} to {end}\n"
        
        summary = []
        summary.append("\n" + "="*70)
        summary.append("ROUTE SUMMARY REPORT")
        summary.append("="*70)
        summary.append(f"\n[TRIP DETAILS]:")
        summary.append(f"   From: {start}")
        summary.append(f"   To:   {end}")
        summary.append(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        summary.append(f"\n[OPTIMIZATION CRITERIA]:")
        summary.append(f"   Optimized for: {optimization.upper()}")
        
        summary.append(f"\n[OPTIMAL ROUTE]:")
        summary.append(f"   {' -> '.join(path)}")
        
        summary.append(f"\n[STATISTICS]:")
        if optimization == "distance":
            summary.append(f"   Total Distance: {stats['actual_distance_km']} km")
            summary.append(f"   Estimated Time: {stats['actual_time_minutes']} minutes")
        elif optimization == "time":
            summary.append(f"   Total Time: {stats['actual_time_minutes']} minutes")
            summary.append(f"   Total Distance: {stats['actual_distance_km']} km")
        else:
            summary.append(f"   Total Cost: {stats['total_cost']} points")
            summary.append(f"   Actual Time: {stats['actual_time_minutes']} minutes")
            summary.append(f"   Distance: {stats['actual_distance_km']} km")
        
        summary.append(f"   Number of Stops: {stats['num_stops']}")
        summary.append(f"   Toll Roads: {stats['total_tolls']}")
        
        # Add turn-by-turn directions
        summary.append(f"\n[TURN-BY-TURN DIRECTIONS]:")
        for i in range(len(path) - 1):
            step_num = i + 1
            current = path[i]
            next_node = path[i + 1]
            
            # Get road info
            road_info = self.get_road_info(current, next_node)
            summary.append(f"   {step_num}. Travel from {current} to {next_node}")
            if road_info:
                summary.append(f"      -> {road_info['distance']} km, {road_info['time']} min")
                if road_info['toll']:
                    summary.append(f"      -> [WARNING] Toll road")
        
        summary.append("\n" + "="*70)
        summary.append("[SUCCESS] Route optimization completed successfully!")
        summary.append("="*70 + "\n")
        
        return "\n".join(summary)
    
    def compare_routes(self, start: str, end: str) -> None:
        """
        Compare different optimization strategies
        
        Args:
            start: Starting location
            end: Destination location
        """
        print("\n" + "="*70)
        print("ROUTE COMPARISON: Different Optimization Strategies")
        print("="*70)
        
        strategies = ["distance", "time", "cost"]
        results = {}
        
        for strategy in strategies:
            path, stats = self.find_route(start, end, strategy)
            if path:
                results[strategy] = {
                    'path': path,
                    'value': stats[list(stats.keys())[0]],
                    'distance': stats['actual_distance_km'],
                    'time': stats['actual_time_minutes'],
                    'tolls': stats['total_tolls']
                }
        
        print(f"\n{'Strategy':<12} {'Value':<12} {'Distance(km)':<12} {'Time(min)':<12} {'Tolls':<8}")
        print("-" * 60)
        for strategy, data in results.items():
            if strategy == "distance":
                value_display = f"{data['value']} km"
            elif strategy == "time":
                value_display = f"{data['value']} min"
            else:
                value_display = f"{data['value']} pts"
            
            print(f"{strategy.capitalize():<12} {value_display:<12} {data['distance']:<12} {data['time']:<12} {data['tolls']:<8}")
        
        # Recommendation
        print("\n[RECOMMENDATION]:")
        time_path = results.get('time', {})
        distance_path = results.get('distance', {})
        
        if time_path and distance_path:
            time_saving = distance_path.get('time', 0) - time_path.get('time', 0)
            if time_saving > 0:
                print(f"   Fastest route saves {time_saving:.1f} minutes compared to shortest distance")
        
        print("\n" + "="*70)