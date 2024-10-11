from priority_queues import PriorityQueueArray, PriorityQueueHeap
import heapq


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
    while previous_node != source:
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
    while previous_node != source:
        path_lst.append(previous_node)
        previous_node = prev[previous_node]

    path_lst.append(source)
    path_lst.reverse()

    cost_of_path = dist[target]

    return path_lst, cost_of_path
