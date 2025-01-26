import matplotlib.pyplot as plt
import networkx as nx
import random
import time

class Graph:
    def __init__(self):
        self.graph = {}
        self._nx_graph = nx.DiGraph()
        
    def generate_random_graph(self, num_nodes):
        if num_nodes <= 0 or num_nodes > 10:
            raise ValueError("Number of nodes must be between 1 and 10")
            
        # Clear existing graph
        self.graph = {}
        self._nx_graph.clear()
        
        # Create nodes A through J (max 10 nodes)
        nodes = [chr(65 + i) for i in range(num_nodes)]
        
        # Generate random edges (ensuring connectivity)
        for i in range(num_nodes - 1):
            # Ensure path from start to end exists
            weight = random.randint(1, 9)
            self.add_edge(nodes[i], nodes[i + 1], weight)
            
            # Add some random additional edges
            for j in range(i + 2, num_nodes):
                if random.random() < 0.4:  # 40% chance of edge
                    weight = random.randint(1, 9)
                    self.add_edge(nodes[i], nodes[j], weight)
        
        return nodes[0], nodes[-1]  # Return start and end nodes

    def add_edge(self, start, end, weight):
        if start not in self.graph:
            self.graph[start] = {}
        self.graph[start][end] = weight
        self._nx_graph.add_edge(start, end, weight=weight)

    def shortest_path(self, start, end):
        if start not in self.graph:
            return float('inf'), []

        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        previous = {vertex: None for vertex in self.graph}
        unvisited = set(self.graph.keys())

        while unvisited:
            current = min(unvisited, key=lambda vertex: distances[vertex])
            
            if current == end or distances[current] == float('inf'):
                break

            unvisited.remove(current)

            for neighbor, weight in self.graph[current].items():
                distance = distances[current] + weight
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    previous[neighbor] = current

        path = []
        current = end
        while current and current in previous:
            path.insert(0, current)
            current = previous[current]
        
        if path and path[0] != start:
            return float('inf'), []
        
        if path:
            path.insert(0, start)

        return distances.get(end, float('inf')), path

    def visualize(self, start=None, end=None, path=None):
        plt.figure(figsize=(12, 6))  # Slightly wider figure
        pos = nx.spring_layout(self._nx_graph, k=1.5)  # Increased spacing
        
        # Add complexity information
        complexity_text = (
            "Dijkstra's Algorithm Complexity:\n"
            f"Time: O(V² + E)\n"
            f"Space: O(V)\n\n"
            f"V (vertices): {len(self._nx_graph.nodes)}\n"
            f"E (edges): {len(self._nx_graph.edges)}\n\n"
            f"Start Node: {start}\n"
            f"End Node: {end}"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                    bbox=dict(facecolor='lightyellow', alpha=0.8),
                    verticalalignment='center')
        
        # Draw nodes
        nx.draw_networkx_nodes(self._nx_graph, pos, node_color='lightblue', 
                             node_size=500)
        nx.draw_networkx_labels(self._nx_graph, pos)
        
        # Draw edges with both weight and edge number
        edge_labels = {}
        for idx, (u, v, data) in enumerate(self._nx_graph.edges(data=True)):
            edge_labels[(u, v)] = f"E{idx+1}:{data['weight']}"
        
        if path and len(path) > 1:
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(self._nx_graph, pos, edgelist=path_edges, 
                                 edge_color='r', width=2)
            other_edges = [(u, v) for (u, v) in self._nx_graph.edges() 
                          if (u, v) not in path_edges]
            nx.draw_networkx_edges(self._nx_graph, pos, edgelist=other_edges, 
                                 edge_color='gray')
        else:
            nx.draw_networkx_edges(self._nx_graph, pos)
            
        # Draw edge labels with both edge number and weight
        nx.draw_networkx_edge_labels(self._nx_graph, pos, edge_labels)
        
        plt.title("Dijkstra's Algorithm Visualization")
        plt.axis('off')
        plt.show()