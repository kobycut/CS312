# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtBeginning(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node


def x_coord(point):
    return point[0]


def find_upper_tangent(L, R):
    l_hull = LinkedList()
    r_hull = LinkedList()
    p = l_hull.head
    q = r_hull.head


def merge(l, r):
    pass


def recursive_helper(points):
    if len(points) < 2:
        return points
    mid = len(points) // 2
    L = recursive_helper(points[:mid])
    R = recursive_helper(points[mid:])
    H = merge(L, R)
    return H


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    sorted_points = sorted(points, key=x_coord)
    H = recursive_helper(sorted_points)

    return [H]


points = []
