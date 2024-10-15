from priority_queues import PriorityQueueArray, PriorityQueueHeap
import heapq
from main import generate_graph
import time
from tabulate import tabulate


def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    dist = {}
    prev = {}
    V = list(graph.keys())
    for node in V:
        dist[node] = float('inf')
        prev[node] = None

    dist[source] = 0
    H = PriorityQueueHeap(V, dist)
    while H.check_empty() != 0:
        U = H.pop_min()
        E = graph[U]
        for connector_node in E.keys():

            if dist[connector_node] > dist[U] + E[connector_node]:
                dist[connector_node] = dist[U] + E[connector_node]
                prev[connector_node] = U
                H.decrease_key(connector_node, dist[connector_node])
    previous_node = target
    path_lst = []
    while previous_node != source and previous_node is not None:
        path_lst.append(previous_node)
        previous_node = prev[previous_node]

    path_lst.append(source)
    path_lst.reverse()
    cost_of_path = dist[target]
    return path_lst, cost_of_path


def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    dist = {}
    prev = {}
    V = list(graph.keys())
    for node in V:
        dist[node] = float('inf')
        prev[node] = None

    dist[source] = 0
    H = PriorityQueueArray(V, dist)
    while H.check_empty() != 0:
        U = H.pop_min()
        E = graph[U]
        for connector_node in E.keys():

            if dist[connector_node] > dist[U] + E[connector_node]:
                dist[connector_node] = dist[U] + E[connector_node]
                prev[connector_node] = U
                H.decrease_key(connector_node, dist[connector_node])
    previous_node = target
    path_lst = []
    while previous_node != source and previous_node is not None:
        path_lst.append(previous_node)
        previous_node = prev[previous_node]

    path_lst.append(source)
    path_lst.reverse()
    cost_of_path = dist[target]
    return path_lst, cost_of_path


def empirical_analysis():
    n_lst = [1000, 2000, 3000, 4000, 5000, 6000]
    density_lst = [1, 1, 1, 1, 1, 1]
    table_data = []
    for i in range(6):


        n = n_lst[i]
        density = density_lst[i]
        _, graph = generate_graph(312, n, density, 0.02)

        array_start_time = time.time()
        array_path, array_cost = find_shortest_path_with_array(graph, 2, 9)
        array_end_time = time.time()
        array_time = array_end_time - array_start_time


        heap_start_time = time.time()
        heap_path, heap_cost = find_shortest_path_with_heap(graph, 2, 9)
        heap_end_time = time.time()
        heap_edges = len(heap_path)
        heap_time = heap_end_time - heap_start_time

        table_data.append([n, density, heap_edges, heap_time, array_time])
        print(i)
    headers = ["n", "density", "# edges", "heap time (s)", "linear time (s)"]
    print(tabulate(table_data, headers=headers, floatfmt=".6f"))



empirical_analysis()