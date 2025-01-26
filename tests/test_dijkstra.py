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
        self.graph.add_edge('A', 'B', 4)
        self.graph.add_edge('A', 'C', 2)
        self.graph.add_edge('B', 'D', 3)
        self.graph.add_edge('C', 'D', 1)
        self.graph.add_edge('C', 'B', 1)
        
        self.assertEqual(self.graph.shortest_path('A', 'D'), (3, ['A', 'C', 'D']))

    def test_no_path(self):
        self.graph.add_edge('A', 'B', 4)
        self.graph.add_edge('C', 'D', 1)
        self.assertEqual(self.graph.shortest_path('A', 'D'), (float('inf'), []))

if __name__ == '__main__':
    unittest.main()