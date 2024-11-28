import copy
import math
import random
import queue
import numpy as np
from matrix import matrix
from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver, score_partial_tour
from tsp_cuttree import CutTree
import heapq


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    cut_tree = CutTree(len(edges))
    bssf = float('inf')
    loop_counter = 0
    while True:
        n_nodes_expanded += 1

        if timer.time_out():
            return stats
        if loop_counter >= len(edges):  # once all nodes visited
            break
        cost = 0
        curr_node = edges[loop_counter]
        visited = [loop_counter]
        path = [loop_counter]
        while True:
            min_weight = float('inf')
            if len(visited) == len(edges):
                cost += curr_node[path[0]]
                break
            for i in range(len(curr_node)):  # loop through out-bound edges
                if curr_node[i] == 0:  # check that isn't path to self
                    continue
                if i in visited:  # check that isn't going back to a visited node
                    continue
                if min_weight > curr_node[i]:
                    min_weight = curr_node[i]  # find minimum cost out-bound edge
                    index = i  # find next node to go to

            if min_weight == float('inf'):  # check if path continues
                cost = float('inf')
                break
            cost += min_weight
            if cost > bssf:
                break

            visited.append(index)
            path.append(index)
            curr_node = edges[index]
            n_nodes_expanded += 1
        if bssf > cost:
            bssf = cost
            bssf_path = path

        loop_counter += 1

    stats.append(SolutionStats(
        tour=bssf_path,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=0,
        n_nodes_pruned=0,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    return stats


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    cut_tree = CutTree(len(edges))
    stats = []
    tour = [0]
    s = [[edges[0], tour]]
    bssf = float('inf')
    bssf_tour = []

    while s:
        if timer.time_out():
            return stats
        if len(tour) == len(edges):
            if score_tour(tour, edges) < bssf:
                bssf = score_tour(tour, edges)
                bssf_tour = tour
            s.pop()

        p_list = s.pop()
        p = p_list[0]
        tour = p_list[1]
        temp_tracking = []
        set_tour = []
        for i in range(len(p)):
            if p[i] == 0:
                continue
            if p[i] == float('inf'):
                continue
            if i in tour:
                continue
            temp_tour = copy.deepcopy(tour)
            temp_tour.append(i)
            temp_tracking.append([edges[i], temp_tour])
            set_tour.append(i)

        if set_tour != float('inf'):
            if not set_tour:
                continue
            tour.append(set_tour[0])
            temp_tracking.reverse()
            for i in temp_tracking:
                s.append(i)

    stats.append(SolutionStats(
        tour=bssf_tour,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=0,
        n_nodes_pruned=0,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    return stats


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    for i in range(len(edges)):
        for j in range(len(edges)):
            if edges[i][j] == 0:
                edges[i][j] = float('inf')

    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    stats = []
    tour = [0]

    initial_matrix = np.array(edges)  # make first initial matrix
    initial_matrix = matrix(initial_matrix, None, None, 0)
    initial_matrix.row_reduce()
    initial_matrix.col_reduce()

    s = [[edges[0], tour, initial_matrix]]
    greedy_results = greedy_tour(edges, timer)  # initial bssf is just the greedy results
    bssf = greedy_results[-1].score
    bssf_tour = greedy_results[-1].tour
    num = 0
    stats.append(SolutionStats(
        tour=bssf_tour,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    while s:
        if timer.time_out():
            print(f"B&B NORMAL: {stats}")
            return stats

        if len(tour) == len(edges):
            if score_tour(tour, edges) < bssf:
                bssf = score_tour(tour, edges)
                bssf_tour = tour
                stats.append(SolutionStats(
                    tour=bssf_tour,
                    score=bssf,
                    time=timer.time(),
                    max_queue_size=0,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            tour = []
            s.pop()
            continue

        p_list = s.pop()
        p = p_list[0]
        tour = p_list[1]
        parent_matrix = p_list[2]
        temp_tracking = []
        set_tour = []

        for i in range(len(p)):
            if p[i] == float('inf'):
                continue
            if i in tour:
                continue
            temp_tour = copy.deepcopy(tour)
            temp_tour.append(i)
            #  figure out row and col... do partial states and get p_lower_bound for p[i]
            p_matrix = copy.deepcopy(parent_matrix)
            p_matrix = matrix(p_matrix.matrix, tour[-1], i, p_matrix.lower_bound)
            p_matrix.lower_bound += parent_matrix.matrix[tour[-1]][i]
            # do all operations on p_matrix
            p_matrix.row_reduce()
            p_matrix.col_reduce()
            p_matrix.cross_out()
            p_matrix.row_reduce()
            p_matrix.col_reduce()
            #  should it be > or >=
            if p_matrix.lower_bound > bssf:
                n_nodes_pruned += 1
                cut_tree.cut(tour)
                continue

            #  if p_lower_bound < lower_bound: add to set, if not, continue
            num += 1
            n_nodes_expanded += 1
            temp_tracking.append([edges[i], temp_tour, p_matrix])
            set_tour.append(i)

        if set_tour != float('inf'):
            if not set_tour:
                continue
            tour.append(set_tour[0])
            temp_tracking.reverse()
            for i in temp_tracking:
                s.append(i)
        # if num % 100 == 0:
        #     print(num)

    stats.append(SolutionStats(
        tour=bssf_tour,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    print(f"NORMAL B&B: {bssf_tour, bssf, timer.time()}")
    return stats


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    for i in range(len(edges)):
        for j in range(len(edges)):
            if edges[i][j] == 0:
                edges[i][j] = float('inf')

    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    stats = []
    tour = [0]

    initial_matrix = np.array(edges)  # make first initial matrix
    initial_matrix = matrix(initial_matrix, None, None, 0)
    initial_matrix.row_reduce()
    initial_matrix.col_reduce()
    #  cities left + lower_bound // 2 for smart pruning
    s = []
    heapq.heappush(s, (0, edges[0], tour, initial_matrix))
    # s = [[edges[0], tour, initial_matrix]]
    greedy_results = greedy_tour(edges, timer)  # initial bssf is just the greedy results
    bssf = greedy_results[-1].score
    bssf_tour = greedy_results[-1].tour
    num = 0
    stats.append(SolutionStats(
        tour=bssf_tour,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    while s:
        if timer.time_out():
            print(f"B&B SMART: {stats}")
            return stats

        if len(tour) == len(edges):
            if score_tour(tour, edges) < bssf:
                bssf = score_tour(tour, edges)
                bssf_tour = tour
                stats.append(SolutionStats(
                    tour=bssf_tour,
                    score=bssf,
                    time=timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            tour = []
            heapq.heappop(s)

            continue
        fake, p, tour, parent_matrix = heapq.heappop(s)
        p_lower_bound = parent_matrix.lower_bound

        temp_tracking = []
        set_tour = []
        if p_lower_bound > bssf:  # if p_lower_bound < lower_bound: do rest, if not, prune
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        for i in range(len(p)):
            if p[i] == float('inf'):
                continue
            if i in tour:
                continue

            temp_tour = copy.deepcopy(tour)
            temp_tour.append(i)
            #  figure out row and col... do partial states and get p_lower_bound for p[i]
            p_matrix = copy.deepcopy(parent_matrix)
            p_matrix = matrix(p_matrix.matrix, tour[-1], i, p_matrix.lower_bound)
            p_matrix.lower_bound += parent_matrix.matrix[tour[-1]][i]
            # do all operations on p_matrix
            p_matrix.row_reduce()
            p_matrix.col_reduce()
            p_matrix.cross_out()
            p_matrix.row_reduce()
            p_matrix.col_reduce()

            if p_matrix.lower_bound >= bssf:
                n_nodes_pruned += 1
                cut_tree.cut(tour)
                continue

            #  if p_lower_bound < lower_bound: add to set, if not, continue

            #  smart technique finds path that has lowest lower_bound and closest to a solution
            num += 1
            n_nodes_expanded += 1
            smart_technique = (p_matrix.lower_bound + (len(edges) - len(tour))) / 2
            # smart_technique = 3
            temp_tracking.append([smart_technique, edges[i], temp_tour, p_matrix])
            set_tour.append(i)

        if set_tour != float('inf'):
            if not set_tour:
                continue
            tour.append(set_tour[0])
            temp_tracking.reverse()
            for i in temp_tracking:
                heapq.heappush(s, i)
        # if num % 100 == 0:
        #     print(num)

    stats.append(SolutionStats(
        tour=bssf_tour,
        score=bssf,
        time=timer.time(),
        max_queue_size=0,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    print(f"SMART B&B:  {bssf_tour, bssf, timer.time()}")
    return stats


# input = [[float('inf'), 7, 3, 12], [3, float('float('inf')'), 6, 14], [5, 8, float('inf'), 6], [9, 3, 5, float('inf')]]
# input = [[float('inf'), 0.8, 0.564, 0.219, float('inf'), 0.595, 0.387, float('inf'), 0.491, float('inf'), 0.588, 0.535,
#           0.674, 0.619, 0.51],
#          [0.8, float('inf'), 0.94, 0.717, 1.08, 0.3, 0.764, 1.144, float('inf'), 0.687, 0.249, float('inf'), 0.207,
#           0.192, 0.414],
#          [0.564, 0.94, float('inf'), 0.377, 0.497, 0.64, 0.93, 0.573, float('inf'), 0.94, float('inf'), 1.069, 0.736,
#           float('inf'), 0.526],
#          [0.219, 0.717, float('inf'), float('inf'), 0.374, float('inf'), 0.555, 0.447, 0.593, 0.563, 0.476, 0.692, 0.55,
#           0.565, 0.349],
#          [0.318, 1.08, 0.497, 0.374, float('inf'), 0.83, 0.669, 0.081, 0.804, 0.723, 0.845, 0.817, 0.923, 0.912, 0.723],
#          [0.595, 0.3, 0.64, 0.456, 0.83, float('inf'), float('inf'), 0.902, 0.59, 0.65, 0.076, 0.774, 0.099, 0.249,
#           0.118],
#          [0.387, float('inf'), 0.93, 0.555, float('inf'), float('inf'), float('inf'), 0.683, 0.208, 0.087, 0.654, 0.15,
#           0.737, 0.576, 0.678],
#          [0.362, 1.144, 0.573, float('inf'), 0.081, 0.902, 0.683, float('inf'), 0.834, 0.744, float('inf'), 0.829,
#           0.993, 0.972, 0.797],
#          [0.491, 0.586, 0.964, 0.593, float('inf'), 0.59, 0.208, 0.834, float('inf'), float('inf'), 0.527, 0.194, 0.6,
#           0.411, 0.599],
#          [0.422, 0.687, 0.94, 0.563, 0.723, 0.65, 0.087, 0.744, 0.12, float('inf'), float('inf'), 0.134, 0.676, 0.503,
#           0.639],
#          [0.588, float('inf'), 0.696, 0.476, 0.845, 0.076, 0.654, 0.913, 0.527, 0.596, float('inf'), 0.715, 0.088,
#           float('inf'), 0.17],
#          [0.535, 0.779, 1.069, 0.692, 0.817, 0.774, 0.15, 0.829, 0.194, 0.134, 0.715, float('inf'), 0.791, float('inf'),
#           float('inf')],
#          [0.674, 0.207, 0.736, 0.55, 0.923, 0.099, 0.737, 0.993, 0.6, 0.676, float('inf'), 0.791, float('inf'), 0.211,
#           float('inf')],
#          [0.619, float('inf'), 0.841, float('inf'), 0.912, 0.249, 0.576, 0.972, 0.411, 0.503, 0.173, 0.605, 0.211,
#           float('inf'), 0.329],
#          [0.51, 0.414, 0.526, 0.349, 0.723, 0.118, float('inf'), 0.797, 0.599, 0.639, 0.17, float('inf'), 0.217, 0.329,
#           float('inf')]]
input = [
    [float('inf'), 0.8, 0.564, 0.219, 0.318, 0.595, 0.387, 0.362, float('inf'), 0.422, float('inf'), 0.535, 0.674,
     float('inf'), 0.51, 0.339, 0.179, float('inf'),
     0.465, 0.5, float('inf'), 0.259, 0.559, 0.123, 0.148, 0.343, 0.668, 0.357, 0.583, 0.453],
    [0.8, float('inf'), 0.94, 0.717, 1.08, 0.3, 0.764, 1.144, 0.586, 0.687, 0.249, 0.779, 0.207, 0.192, 0.414, 1.04,
     0.961,
     0.513, 0.568, 0.82, 0.891, float('inf'), 0.242, 0.915, 0.672, 0.76, 0.762, 1.158, 0.608, 0.906],
    [0.564, float('inf'), float('inf'), 0.377, float('inf'), float('inf'), 0.93, 0.573, 0.964, 0.94, 0.696, 1.069,
     0.736, 0.841, 0.526, 0.87, 0.518, 0.922,
     float('inf'), 0.12, 0.556, 0.78, 0.764, 0.632, 0.635, float('inf'), 0.27, 0.7, 1.057, 0.114],
    [0.219, 0.717, 0.377, float('inf'), float('inf'), 0.456, 0.555, 0.447, 0.593, float('inf'), 0.476, 0.692, 0.55,
     0.565, 0.349, 0.557, 0.285,
     0.558, 0.262, 0.293, 0.26, 0.474, 0.491, 0.326, 0.258, float('inf'), 0.45, 0.506, 0.687, 0.279],
    [0.318, float('inf'), 0.497, 0.374, float('inf'), 0.83, 0.669, 0.081, 0.804, 0.723, 0.845, 0.817, 0.923,
     float('inf'), 0.723, 0.451, 0.141,
     0.802, 0.617, 0.505, 0.232, 0.368, 0.844, 0.271, 0.465, 0.627, float('inf'), 0.206, float('inf'), float('inf')],
    [0.595, 0.3, 0.64, 0.456, 0.83, float('inf'), 0.702, 0.902, 0.59, 0.65, float('inf'), 0.774, float('inf'), 0.249,
     float('inf'), 0.895, float('inf'), 0.516, float('inf'),
     0.52, 0.676, 0.835, 0.192, 0.718, 0.502, 0.682, 0.473, 0.943, 0.654, 0.61],
    [0.387, 0.764, 0.93, 0.555, 0.669, 0.702, float('inf'), 0.683, 0.208, 0.087, 0.654, float('inf'), 0.737, 0.576,
     0.678, 0.346, 0.533,
     0.262, 0.717, 0.846, 0.445, 0.362, 0.56, 0.398, 0.298, 0.044, 0.971, 0.603, float('inf'), 0.825],
    [0.362, 1.144, 0.573, 0.447, 0.081, 0.902, float('inf'), float('inf'), 0.834, 0.744, 0.913, float('inf'), 0.993,
     0.972, 0.797, 0.428, 0.186,
     0.838, 0.695, float('inf'), 0.27, 0.353, 0.906, 0.289, 0.51, 0.642, 0.793, 0.147, 0.92, 0.473],
    [0.491, 0.586, 0.964, float('inf'), float('inf'), 0.59, 0.208, 0.834, float('inf'), 0.12, float('inf'), 0.194, 0.6,
     0.411, 0.599, float('inf'), 0.663, 0.076,
     0.681, 0.863, 0.572, 0.549, 0.416, 0.546, 0.356, 0.227, float('inf'), 0.777, 0.094, 0.872],
    [0.422, 0.687, float('inf'), 0.563, 0.723, 0.65, float('inf'), 0.744, 0.12, float('inf'), 0.596, 0.134, 0.676,
     0.503, 0.639, 0.43, 0.584,
     0.178, float('inf'), 0.848, float('inf'), 0.439, 0.495, float('inf'), 0.308, 0.111, 0.957, 0.674, 0.182,
     float('inf')],
    [0.588, 0.249, 0.696, 0.476, 0.845, 0.076, 0.654, 0.913, float('inf'), 0.596, float('inf'), 0.715, float('inf'),
     0.173, 0.17, 0.87, 0.735, float('inf'),
     0.323, 0.576, 0.674, 0.816, 0.119, float('inf'), 0.48, 0.637, 0.544, 0.942, float('inf'), 0.657],
    [0.535, 0.779, 1.069, 0.692, 0.817, 0.774, 0.15, float('inf'), 0.194, 0.134, 0.715, float('inf'), 0.791,
     float('inf'), 0.769, 0.463, 0.683,
     float('inf'), 0.83, 0.98, 0.595, 0.496, 0.607, 0.546, 0.435, float('inf'), 1.091, 0.74, 0.189, 0.967],
    [0.674, float('inf'), 0.736, 0.55, 0.923, 0.099, 0.737, 0.993, 0.6, 0.676, 0.088, float('inf'), float('inf'), 0.211,
     0.217, float('inf'), 0.816, float('inf'),
     float('inf'), 0.617, 0.758, 0.904, 0.184, 0.795, 0.568, 0.722, float('inf'), 1.027, 0.652, 0.709],
    [0.619, 0.192, 0.841, 0.565, 0.912, 0.249, 0.576, 0.972, float('inf'), float('inf'), 0.173, 0.605, 0.211,
     float('inf'), float('inf'), 0.848, 0.787,
     0.335, 0.474, 0.722, 0.712, 0.81, 0.077, 0.73, 0.485, 0.57, float('inf'), 0.975, 0.45, 0.788],
    [0.51, 0.414, 0.526, 0.349, 0.723, 0.118, 0.678, 0.797, float('inf'), 0.639, float('inf'), 0.769, 0.217, 0.329,
     float('inf'), 0.828, 0.629,
     float('inf'), 0.154, 0.406, 0.584, 0.761, 0.257, 0.633, 0.439, float('inf'), 0.385, 0.847, 0.675, 0.493],
    [0.339, 1.04, 0.87, float('inf'), 0.451, 0.895, 0.346, 0.428, 0.548, 0.43, 0.87, 0.463, 0.958, float('inf'), 0.828,
     float('inf'), 0.36, float('inf'),
     float('inf'), 0.826, 0.315, 0.09, float('inf'), 0.24, 0.393, 0.321, 1.005, 0.304, 0.61, 0.756],
    [0.179, 0.961, 0.518, 0.285, 0.141, 0.729, 0.533, 0.186, 0.663, 0.584, 0.735, 0.683, 0.816, 0.787, 0.629, 0.36,
     float('inf'),
     float('inf'), 0.545, 0.493, 0.091, 0.27, 0.722, 0.142, float('inf'), 0.49, 0.69, 0.222, 0.753, 0.405],
    [0.484, 0.513, 0.922, 0.558, float('inf'), float('inf'), 0.262, float('inf'), 0.076, 0.178, float('inf'), 0.27,
     0.524, 0.335, 0.531, 0.587, 0.661, float('inf'),
     0.621, float('inf'), 0.571, 0.577, 0.34, 0.554, 0.34, 0.271, 0.888, 0.793, 0.144, 0.834],
    [0.465, 0.568, 0.373, 0.262, 0.617, 0.269, 0.717, 0.695, 0.681, 0.696, 0.323, 0.83, 0.367, 0.474, 0.154, 0.801,
     0.545, 0.621, float('inf'), 0.253, 0.52, 0.724, 0.399, 0.581, 0.439, 0.684, float('inf'), 0.766, 0.765, 0.343],
    [0.5, 0.82, 0.12, float('inf'), 0.505, 0.52, 0.846, 0.585, 0.863, 0.848, float('inf'), 0.98, 0.617, 0.722, 0.406,
     float('inf'), 0.493, 0.816,
     0.253, float('inf'), float('inf'), 0.738, 0.645, float('inf'), 0.548, 0.805, 0.209, float('inf'), 0.954, 0.124],
    [0.093, 0.891, 0.556, 0.26, float('inf'), 0.676, 0.445, float('inf'), 0.572, 0.493, 0.674, 0.595, 0.758, 0.712,
     0.584, 0.315, float('inf'),
     float('inf'), 0.52, 0.512, float('inf'), 0.226, 0.65, 0.075, float('inf'), float('inf'), 0.697, 0.269, 0.662,
     float('inf')],
    [0.259, 1.001, 0.78, float('inf'), 0.368, 0.835, 0.362, float('inf'), 0.549, 0.439, 0.816, 0.496, 0.904,
     float('inf'), 0.761, float('inf'), 0.27, 0.577,
     0.724, 0.738, 0.226, float('inf'), 0.764, 0.151, 0.336, 0.328, 0.919, float('inf'), 0.621, 0.666],
    [0.559, 0.242, 0.764, 0.491, 0.844, 0.192, 0.56, 0.906, 0.416, float('inf'), 0.119, 0.607, 0.184, 0.077, 0.257,
     0.808, 0.722,
     0.34, 0.399, 0.645, float('inf'), 0.764, float('inf'), 0.673, 0.431, 0.548, 0.642, 0.916, 0.47, 0.711],
    [0.123, 0.915, 0.632, 0.326, 0.271, 0.718, 0.398, float('inf'), 0.546, 0.455, 0.709, 0.546, 0.795, 0.73, 0.633,
     0.24, 0.142,
     float('inf'), 0.581, 0.586, 0.075, 0.151, float('inf'), float('inf'), 0.246, 0.356, 0.769, 0.247, 0.631,
     float('inf')],
    [0.148, 0.672, 0.635, float('inf'), 0.465, 0.502, 0.298, 0.51, 0.356, 0.308, 0.48, 0.435, float('inf'), 0.485,
     0.439, 0.393, 0.326,
     0.34, 0.439, 0.548, 0.24, 0.336, 0.431, 0.246, float('inf'), float('inf'), 0.681, 0.493, float('inf'),
     float('inf')],
    [float('inf'), float('inf'), 0.888, 0.514, 0.627, 0.682, 0.044, 0.642, 0.227, 0.111, 0.637, 0.193, float('inf'),
     0.57, 0.651, 0.321, float('inf'),
     0.271, 0.684, 0.805, 0.402, 0.328, float('inf'), 0.356, 0.258, float('inf'), 0.935, float('inf'), 0.293, 0.782],
    [float('inf'), 0.762, float('inf'), 0.45, 0.713, float('inf'), float('inf'), 0.793, 0.947, 0.957, 0.544, 1.091,
     0.556, 0.712, 0.385, 1.005, 0.69, 0.888,
     0.266, 0.209, float('inf'), 0.919, 0.642, 0.769, 0.681, 0.935, float('inf'), 0.9, 1.032, float('inf')],
    [0.357, float('inf'), 0.7, float('inf'), 0.206, 0.943, 0.603, 0.147, 0.777, 0.674, 0.942, 0.74, float('inf'), 0.975,
     0.847, 0.304, 0.222,
     0.793, 0.766, 0.696, 0.269, 0.246, 0.916, 0.247, 0.493, 0.566, 0.9, float('inf'), 0.856, float('inf')],
    [float('inf'), 0.608, 1.057, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 0.094, 0.182,
     0.586, 0.189, 0.652, float('inf'), float('inf'), 0.61, 0.753, 0.144, 0.765,
     0.954, 0.662, 0.621, 0.47, 0.631, 0.45, 0.293, 1.032, 0.856, float('inf'), float('inf')],
    [0.453, 0.906, 0.114, float('inf'), float('inf'), float('inf'), 0.825, 0.473, 0.872, 0.84, 0.657, 0.967, 0.709,
     0.788, 0.493, 0.756, 0.405,
     float('inf'), 0.343, 0.124, float('inf'), 0.666, 0.711, 0.518, 0.532, 0.782, 0.33, 0.593, 0.965, float('inf')]]
# print(branch_and_bound(input, Timer()))
# print(branch_and_bound_smart(input, Timer()))
