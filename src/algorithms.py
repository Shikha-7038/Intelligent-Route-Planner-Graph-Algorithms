"""
Graph algorithms implementation
Includes BFS, DFS, and Dijkstra's algorithm with priority queue
"""

import heapq
from typing import Dict, List, Set, Tuple, Optional, Callable
from collections import deque

class GraphAlgorithms:
    """Class containing all graph algorithms"""
    
    def __init__(self, graph):
        """
        Initialize with a graph object
        
        Args:
            graph: Graph object from graph.py
        """
        self.graph = graph
    
    def bfs(self, start: str, end: str) -> Optional[List[str]]:
        """
        Breadth-First Search to find path (unweighted)
        
        Args:
            start: Starting node
            end: Destination node
            
        Returns:
            List of nodes representing the path, or None if no path exists
        """
        if start not in self.graph.adjacency_list or end not in self.graph.adjacency_list:
            return None
        
        visited = set()
        queue = deque([(start, [start])])
        
        while queue:
            node, path = queue.popleft()
            
            if node == end:
                return path
            
            if node not in visited:
                visited.add(node)
                for neighbor, _, _, _, _ in self.graph.get_neighbors(node):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def dfs(self, start: str, end: str) -> Optional[List[str]]:
        """
        Depth-First Search to find path (unweighted)
        
        Args:
            start: Starting node
            end: Destination node
            
        Returns:
            List of nodes representing the path, or None if no path exists
        """
        if start not in self.graph.adjacency_list or end not in self.graph.adjacency_list:
            return None
        
        visited = set()
        stack = [(start, [start])]
        
        while stack:
            node, path = stack.pop()
            
            if node == end:
                return path
            
            if node not in visited:
                visited.add(node)
                for neighbor, _, _, _, _ in self.graph.get_neighbors(node):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        
        return None
    
    def dijkstra(self, start: str, end: str, weight_type: str = "distance") -> Tuple[Optional[List[str]], float]:
        """
        Dijkstra's algorithm for shortest path in weighted graph
        
        Args:
            start: Starting node
            end: Destination node
            weight_type: Type of weight ("distance", "time", "cost")
            
        Returns:
            Tuple of (path list, total weight)
        """
        if start not in self.graph.adjacency_list or end not in self.graph.adjacency_list:
            return None, float('inf')
        
        # Priority queue: (distance, node, path)
        pq = [(0, start, [start])]
        visited = set()
        distances = {node: float('inf') for node in self.graph.adjacency_list}
        distances[start] = 0
        
        while pq:
            current_dist, current_node, path = heapq.heappop(pq)
            
            if current_node == end:
                return path, current_dist
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            for neighbor, distance, time, road_type, toll in self.graph.get_neighbors(current_node):
                # Get weight based on type
                if weight_type == "distance":
                    weight = distance
                elif weight_type == "time":
                    weight = time
                elif weight_type == "cost":
                    weight = time + (toll * 2)  # Toll adds time penalty
                else:
                    weight = distance
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))
        
        return None, float('inf')
    
    def dijkstra_with_turn_penalty(self, start: str, end: str, turn_penalty: float = 1.0) -> Tuple[Optional[List[str]], float]:
        """
        Dijkstra's algorithm with turn penalties
        
        Args:
            start: Starting node
            end: Destination node
            turn_penalty: Penalty for changing direction
            
        Returns:
            Tuple of (path list, total weight)
        """
        if start not in self.graph.adjacency_list or end not in self.graph.adjacency_list:
            return None, float('inf')
        
        # State: (node, previous_node) -> best distance
        # Priority queue: (distance, node, prev_node, path)
        pq = [(0, start, None, [start])]
        visited_states = {}
        
        while pq:
            current_dist, current_node, prev_node, path = heapq.heappop(pq)
            
            state = (current_node, prev_node)
            if state in visited_states and visited_states[state] <= current_dist:
                continue
            visited_states[state] = current_dist
            
            if current_node == end:
                return path, current_dist
            
            for neighbor, distance, time, road_type, toll in self.graph.get_neighbors(current_node):
                # Calculate turn penalty if applicable
                penalty = 0
                if prev_node is not None and len(path) >= 2:
                    # Check if direction changed
                    prev_prev = path[-2]
                    # Simple heuristic: if it's a turn (not straight line)
                    # In real implementation, you'd check angles
                    penalty = turn_penalty
                
                weight = time + (toll * 2) + penalty
                new_dist = current_dist + weight
                
                heapq.heappush(pq, (new_dist, neighbor, current_node, path + [neighbor]))
        
        return None, float('inf')
    
    def get_all_paths(self, start: str, end: str, max_paths: int = 5) -> List[Tuple[List[str], float]]:
        """
        Find multiple paths between start and end
        
        Args:
            start: Starting node
            end: Destination node
            max_paths: Maximum number of paths to find
            
        Returns:
            List of tuples (path, total_weight)
        """
        paths = []
        visited_nodes = set()
        
        # Modified Dijkstra that stores multiple paths
        pq = [(0, start, [start])]
        path_count = 0
        
        while pq and path_count < max_paths:
            current_dist, current_node, path = heapq.heappop(pq)
            
            if current_node == end:
                paths.append((path, current_dist))
                path_count += 1
                continue
            
            if current_node in visited_nodes and path_count > 0:
                continue
            
            visited_nodes.add(current_node)
            
            for neighbor, distance, time, road_type, toll in self.graph.get_neighbors(current_node):
                if neighbor not in path:  # Avoid cycles
                    weight = time
                    new_dist = current_dist + weight
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))
        
        return paths
    
    def compare_algorithms(self, start: str, end: str) -> None:
        """
        Compare BFS, DFS, and Dijkstra results
        
        Args:
            start: Starting node
            end: Destination node
        """
        print("\n" + "="*60)
        print(f"ALGORITHM COMPARISON: {start} → {end}")
        print("="*60)
        
        # BFS
        bfs_path = self.bfs(start, end)
        print(f"\nBFS Path (Unweighted): {bfs_path}")
        print(f"BFS Path Length: {len(bfs_path) if bfs_path else 0} nodes")
        
        # DFS
        dfs_path = self.dfs(start, end)
        print(f"\nDFS Path (Unweighted): {dfs_path}")
        print(f"DFS Path Length: {len(dfs_path) if dfs_path else 0} nodes")
        
        # Dijkstra - Distance
        dijkstra_dist_path, dist_total = self.dijkstra(start, end, "distance")
        print(f"\nDijkstra (Shortest Distance): {dijkstra_dist_path}")
        print(f"Total Distance: {dist_total} km")
        
        # Dijkstra - Time
        dijkstra_time_path, time_total = self.dijkstra(start, end, "time")
        print(f"\nDijkstra (Fastest Time): {dijkstra_time_path}")
        print(f"Total Time: {time_total} minutes")
        
        # Dijkstra - Cost
        dijkstra_cost_path, cost_total = self.dijkstra(start, end, "cost")
        print(f"\nDijkstra (Minimum Cost): {dijkstra_cost_path}")
        print(f"Total Cost: {cost_total} (time + toll penalty)")