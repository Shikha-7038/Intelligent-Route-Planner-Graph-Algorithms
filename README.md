# 🗺️ Intelligent Route Planner Using Graph Algorithms

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Graph Algorithms](https://img.shields.io/badge/Graph-Dijkstra-red.svg)](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

## 📋 Project Overview

An **Intelligent Route Planning System** that finds optimal paths between locations using classical graph algorithms. This project demonstrates how real-world navigation systems like Google Maps, Uber, and logistics platforms work under the hood.

### 🎯 What Problem Does It Solve?

Finding the most efficient route between two locations considering:
- **Shortest distance** - Minimize travel distance
- **Fastest time** - Minimize travel duration  
- **Minimum cost** - Avoid toll roads and expensive routes

### 🏗️ How It Works
Locations (Nodes) → Roads (Edges) → Weights → Dijkstra's Algorithm → Optimal Route

text

## 🚀 Features

- ✅ Graph representation using **Adjacency List**
- ✅ **Dijkstra's Algorithm** with priority queue (min heap)
- ✅ **BFS & DFS** traversal for unweighted pathfinding
- ✅ Multiple optimization criteria (distance, time, cost)
- ✅ Route comparison and analysis
- ✅ Turn-by-turn directions
- ✅ Graph visualization (optional with matplotlib/networkx)
- ✅ Interactive CLI interface
- ✅ Route summary export

## 📁 DSA Concepts Used

| Concept | Implementation |
|---------|---------------|
| **Graphs** | Road network representation |
| **Adjacency List** | Memory-efficient graph storage |
| **Dijkstra's Algorithm** | Shortest path in weighted graphs |
| **Priority Queue / Min Heap** | Optimal node selection |
| **BFS** | Unweighted shortest path |
| **DFS** | Graph traversal |
| **Path Reconstruction** | Building the final route |

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Core Libraries**: heapq, csv, collections
- **Visualization** (optional): networkx, matplotlib
- **Testing**: pytest

## 📂 Folder Structure
Intelligent-Route-Planner-Graph-Algorithms/
│
├── data/ # Dataset files
│ ├── locations.csv # Node coordinates
│ └── roads.csv # Edge weights
│
├── src/ # Source code
│ ├── graph.py # Graph class & adjacency list
│ ├── algorithms.py # BFS, DFS, Dijkstra
│ ├── route_planner.py # Route optimization
│ ├── visualization.py # Graph plotting
│ └── utils.py # Helper functions
│
├── outputs/ # Generated outputs
│ └── route_output.txt # Route summaries
│
├── images/ # Screenshots for GitHub
│
├── main.py # Entry point
├── requirements.txt # Dependencies
└── README.md # Documentation

text

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/Intelligent-Route-Planner-Graph-Algorithms.git
cd Intelligent-Route-Planner-Graph-Algorithms
Step 2: Create Virtual Environment (Recommended)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Run the Application
bash
python main.py
💻 How to Use
Sample Input/Output
text
==================================================
  INTELLIGENT ROUTE PLANNER
==================================================

Available locations: A, B, C, D, E, F, G, H, I, J

Enter source location: A
Enter destination location: H

🔄 Finding optimal route...

==================================================
✓ OPTIMAL ROUTE FOUND!
==================================================

Route: A → B → D → E → G → H

Statistics:
  Total Distance: 14.2 km
  Total Time: 31 minutes
  Toll Roads: 2

Turn-by-Turn Directions:
1. Travel from A to B (2.5 km, 5 min)
2. Travel from B to D (3.2 km, 6 min) → ⚠️ Toll road
3. Travel from D to E (1.5 km, 3 min)
4. Travel from E to G (3.0 km, 7 min) → ⚠️ Toll road
5. Travel from G to H (2.5 km, 5 min)
Menu Options
text
1. Find Shortest Path (Distance)
2. Find Fastest Path (Time)
3. Find Cheapest Path (Cost)
4. Compare Different Routes
5. Show All Available Locations
6. Show Adjacency List
7. Run BFS/DFS Traversal
8. Visualize Graph
9. Compare Algorithms
0. Exit
📊 Sample Outputs
Adjacency List Representation
text
A -> [B: 2.5km, 5min, local] 
B -> [A: 2.5km, 5min, local] [C: 1.8km, 4min, local] [D: 3.2km, 6min, highway, TOLL] [J: 2.0km, 5min, local]
Dijkstra Algorithm Result
text
Shortest Path (Distance): A → B → D → E → G → H
Total Distance: 14.2 km
Route Comparison
text
Strategy    Value        Distance(km)  Time(min)    Tolls   
------------------------------------------------------------
Distance    14.2 km      14.2          33.0         2       
Time        31.0 min     15.0          31.0         2       
Cost        29.0 pts     14.2          31.0         1       

💡 RECOMMENDATION: Fastest route saves 2.0 minutes compared to shortest distance
🎓 Learning Outcomes
After this project, you will understand:

Graph Theory Fundamentals - Nodes, edges, weights, directed vs undirected

Dijkstra's Algorithm - How it works, why priority queue is used

Time Complexity Analysis - O((V+E) log V) for Dijkstra with heap

Path Reconstruction - Building the actual path from algorithm output

Real-world Applications - How maps and navigation systems work

📈 Future Improvements
Add A* algorithm with heuristic

Implement real-time traffic conditions

Add multiple route alternatives

Create web interface with Flask/FastAPI

Integrate with OpenStreetMap data

Add turn restrictions and penalties
