import copy
import math
import random
import queue

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


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
    n_nodes_pruned = 0
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
    tour = [0]
    s = [[edges[0], tour]]
    bssf = float('inf')
    bssf_tour = []

    while s:
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

    return []


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
