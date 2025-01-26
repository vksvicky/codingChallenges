import unittest
from src.dijkstra import Graph

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_empty_graph(self):
        self.assertEqual(self.graph.shortest_path('A', 'B'), (float('inf'), []))

    def test_single_path(self):
        self.graph.add_edge('A', 'B', 4)
        self.assertEqual(self.graph.shortest_path('A', 'B'), (4, ['A', 'B']))

    def test_complex_path(self):
        graph = Graph()
        # Create a more complex graph with multiple possible paths
        graph.add_edge('A', 'B', 4)
        graph.add_edge('A', 'C', 2)
        graph.add_edge('B', 'D', 3)
        graph.add_edge('C', 'D', 1)
        graph.add_edge('C', 'E', 5)
        graph.add_edge('D', 'E', 2)
        
        distance, path = graph.shortest_path('A', 'E')
        self.assertEqual(path, ['A', 'C', 'D', 'E'])
        self.assertEqual(distance, 5)  # A->C(2) + C->D(1) + D->E(2) = 5

    def test_no_path(self):
        self.graph.add_edge('A', 'B', 4)
        self.graph.add_edge('C', 'D', 1)
        self.assertEqual(self.graph.shortest_path('A', 'D'), (float('inf'), []))

if __name__ == '__main__':
    unittest.main()