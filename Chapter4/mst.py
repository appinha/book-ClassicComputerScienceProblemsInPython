# Minimum (Weight) Spanning Tree

from typing import List, Optional, TypeVar
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue


V = TypeVar('V')  # type of the vertices in the graph
WeightedPath = List[WeightedEdge]  # type alias for paths


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start < 0 or start > (wg.vertex_count - 1):
        return None

    result: WeightedPath = []
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: List[bool] = wg.vertex_count * [False]

    def visit(index: int):
        visited[index] = True  # mark as visited
        # add to pq all edges coming from vertex to vertices not visited
        for edge in wg.edges_for_index(index):
            if not visited[edge.v]:
                pq.push(edge)

    visit(start)  # the first vertex is where everything begins

    while not pq.is_empty:  # keep going while there are edges to process
        edge = pq.pop()  # gets current smallest edge from priority queue
        if visited[edge.v]:
            continue  # don't revisit vertices
        result.append(edge)  # add edge to solution
        visit(edge.v)  # visit where this connects

    return result


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f'{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}')
    print(f'Total weight: {total_weight(wp)}')


if __name__ == '__main__':
    city_weighted_graph: WeightedGraph[str] = WeightedGraph([
        "Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix", "Chicago", "Boston",
        "New York", "Atlanta", "Miami", "Dallas", "Houston", "Detroit", "Philadelphia", "Washington"
    ])

    city_weighted_graph.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_weighted_graph.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_weighted_graph.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_weighted_graph.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_weighted_graph.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_weighted_graph.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_weighted_graph.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_weighted_graph.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_weighted_graph.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_weighted_graph.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_weighted_graph.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_weighted_graph.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_weighted_graph.add_edge_by_vertices("Dallas", "Houston", 225)
    city_weighted_graph.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_weighted_graph.add_edge_by_vertices("Houston", "Miami", 968)
    city_weighted_graph.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_weighted_graph.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_weighted_graph.add_edge_by_vertices("Atlanta", "Miami", 604)
    city_weighted_graph.add_edge_by_vertices("Miami", "Washington", 923)
    city_weighted_graph.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_weighted_graph.add_edge_by_vertices("Detroit", "Boston", 613)
    city_weighted_graph.add_edge_by_vertices("Detroit", "Washington", 396)
    city_weighted_graph.add_edge_by_vertices("Detroit", "New York", 482)
    city_weighted_graph.add_edge_by_vertices("Boston", "New York", 190)
    city_weighted_graph.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_weighted_graph.add_edge_by_vertices("Philadelphia", "Washington", 123)

    result: Optional[WeightedPath] = mst(city_weighted_graph)
    if result is None:
        print('No solution found!')
    else:
        print_weighted_path(city_weighted_graph, result)
