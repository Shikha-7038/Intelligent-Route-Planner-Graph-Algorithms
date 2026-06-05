"""
Utility functions for the route planner
"""

import csv
import os
from typing import List, Dict, Tuple

def validate_location(location: str, graph) -> bool:
    """
    Validate if a location exists in the graph
    
    Args:
        location: Location name
        graph: Graph object
        
    Returns:
        True if location exists, False otherwise
    """
    return location in graph.adjacency_list

def get_all_locations(graph) -> List[str]:
    """
    Get all available locations
    
    Args:
        graph: Graph object
        
    Returns:
        List of all location names
    """
    return list(graph.adjacency_list.keys())

def format_duration(minutes: float) -> str:
    """
    Format duration in minutes to readable string
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted string (e.g., "1 hour 30 minutes")
    """
    if minutes < 60:
        return f"{minutes:.0f} minutes"
    else:
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if mins > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {mins} minutes"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''}"

def format_distance(km: float) -> str:
    """
    Format distance in km to readable string
    
    Args:
        km: Distance in kilometers
        
    Returns:
        Formatted string (e.g., "15.5 km")
    """
    if km < 1:
        return f"{km * 1000:.0f} meters"
    else:
        return f"{km:.1f} km"

def save_route_to_file(route_summary: str, filename: str = "outputs/route_output.txt"):
    """
    Save route summary to a text file
    
    Args:
        route_summary: Route summary string
        filename: Output filename
    """
    # Create outputs directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Remove emoji characters for Windows compatibility
    import re
    # Remove emoji and special Unicode characters
    route_summary_clean = re.sub(r'[^\x00-\x7F]+', '', route_summary)
    # Replace common emoji with text equivalents
    route_summary_clean = route_summary_clean.replace('📍', '[LOCATION]')
    route_summary_clean = route_summary_clean.replace('🗺️', '[ROUTE]')
    route_summary_clean = route_summary_clean.replace('📊', '[STATS]')
    route_summary_clean = route_summary_clean.replace('🎯', '[OPTIMIZATION]')
    route_summary_clean = route_summary_clean.replace('📋', '[DIRECTIONS]')
    route_summary_clean = route_summary_clean.replace('✅', '[SUCCESS]')
    route_summary_clean = route_summary_clean.replace('⚠️', '[WARNING]')
    route_summary_clean = route_summary_clean.replace('→', '->')
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(route_summary_clean)
    print(f"✓ Route summary saved to {filename}")

def create_sample_dataset():
    """
    Create sample dataset files if they don't exist
    """
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Create locations.csv if it doesn't exist
    locations_file = 'data/locations.csv'
    if not os.path.exists(locations_file):
        with open(locations_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['location', 'lat', 'lon'])
            sample_locations = [
                ['A', 12.9716, 77.5946],
                ['B', 12.9750, 77.6000],
                ['C', 12.9800, 77.5950],
                ['D', 12.9780, 77.6100],
                ['E', 12.9900, 77.6150],
                ['F', 12.9850, 77.6200],
                ['G', 12.9950, 77.6250],
                ['H', 13.0000, 77.6300],
                ['I', 12.9880, 77.6050],
                ['J', 12.9820, 77.5980],
            ]
            writer.writerows(sample_locations)
        print(f"✓ Created sample {locations_file}")
    
    # Create roads.csv if it doesn't exist
    roads_file = 'data/roads.csv'
    if not os.path.exists(roads_file):
        with open(roads_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['source', 'destination', 'distance', 'time', 'road_type', 'toll'])
            sample_roads = [
                ['A', 'B', 2.5, 5, 'local', 0],
                ['B', 'A', 2.5, 5, 'local', 0],
                ['B', 'C', 1.8, 4, 'local', 0],
                ['C', 'B', 1.8, 4, 'local', 0],
                ['B', 'D', 3.2, 6, 'highway', 1],
                ['D', 'B', 3.2, 6, 'highway', 1],
                ['C', 'E', 2.0, 4, 'highway', 0],
                ['E', 'C', 2.0, 4, 'highway', 0],
                ['D', 'E', 1.5, 3, 'local', 0],
                ['E', 'D', 1.5, 3, 'local', 0],
                ['E', 'F', 2.2, 5, 'local', 0],
                ['F', 'E', 2.2, 5, 'local', 0],
                ['E', 'G', 3.0, 7, 'highway', 1],
                ['G', 'E', 3.0, 7, 'highway', 1],
                ['F', 'G', 1.8, 4, 'local', 0],
                ['G', 'F', 1.8, 4, 'local', 0],
                ['G', 'H', 2.5, 5, 'local', 0],
                ['H', 'G', 2.5, 5, 'local', 0],
                ['D', 'I', 2.8, 6, 'local', 0],
                ['I', 'D', 2.8, 6, 'local', 0],
                ['I', 'E', 1.2, 3, 'local', 0],
                ['E', 'I', 1.2, 3, 'local', 0],
                ['I', 'J', 1.5, 3, 'local', 0],
                ['J', 'I', 1.5, 3, 'local', 0],
                ['J', 'B', 2.0, 5, 'local', 0],
                ['B', 'J', 2.0, 5, 'local', 0],
            ]
            writer.writerows(sample_roads)
        print(f"✓ Created sample {roads_file}")

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_footer():
    """Print a formatted footer"""
    print("="*70 + "\n")