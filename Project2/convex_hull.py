# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


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

        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node


def x_coord(point):
    return point[0]


def get_slope(x1, x2, y1, y2):
    return (y2 - y1) / (x2 - x1)

def find_lower_tangent(l, r):
    l_hull = LinkedList()
    r_hull = LinkedList()
    l = sorted(l, key=x_coord)
    r = sorted(r, key=x_coord, reverse=True)
    for i in l:
        l_hull.insertAtBeginning(i)
    for j in r:
        r_hull.insertAtBeginning(j)
    p = l_hull.head
    q = r_hull.head
    temp = (p, q)
    done = False
    while not done:
        done = True
        while True:
            temp_slope = get_slope(temp[0][0], temp[1][0], temp[0][1], temp[1][1])
            l_slope = get_slope(p[0], l_hull.head.data[0], p[1], l_hull.head.data[1])
            if temp_slope > l_slope:
                r = p.prev
                temp = (r,q)
                p = r
                done = False
            else:
                break
        while True:
            temp_slope = get_slope(temp[0][0], temp[1][0], temp[0][1], temp[1][1])
            r_slope = get_slope(q[0], r_hull.head.data[0], q[1], r_hull.head.data[1])
            if temp_slope > r_slope:
                r = q.prev
                temp = (p, r)
                q = r
                done = False
            else:
                break
    return temp
def find_upper_tangent(l, r):
    l_hull = LinkedList()
    r_hull = LinkedList()
    l = sorted(l, key=x_coord)
    r = sorted(r, key=x_coord, reverse=True)
    for i in l:
        l_hull.insertAtBeginning(i)
    for j in r:
        r_hull.insertAtBeginning(j)
    p = l_hull.head
    q = r_hull.head
    temp = (p, q)
    done = False
    while not done:
        done = True
        while True:
            temp_slope = get_slope(temp[0][0], temp[1][0], temp[0][1], temp[1][1])
            l_slope =
            if temp_slope > l_slope:
                r = p.next
                temp = (r,q)
                p = r
                done = False
            else:
                break
        while True:
            temp_slope = get_slope(temp[0][0], temp[1][0], temp[0][1], temp[1][1])
            r_slope =
            if temp_slope > r_slope:
                r = q.next
                temp = (p, r)
                q = r
                done = False
            else:
                break
    return temp

def merge(l, r):
    upper_tangent = find_upper_tangent(l, r)
    lower_tangent = find_lower_tangent(l, r)
    return upper_tangent, lower_tangent


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


points = [(1, 324), (2, 363), (3, 211), (4, 54), (5, 93)]
print(compute_hull(points))
