# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self):
        return self.data


class LinkedList:
    def __init__(self, tail, head):
        self.head = head
        self.tail = tail


def count_nodes(head):
    data = head.get_data()
    size = 1
    while True:
        head = head.next
        if data == head.get_data():
            break
        size += 1
    return size


def x_coord(point):
    return point[0]


def get_slope(x1, x2, y1, y2):
    return (y2 - y1) / (x2 - x1)


def find_upper_tangent(l, r):
    p = l.head
    q = r.tail
    px = p.get_data()[0]
    py = p.get_data()[1]
    qx = q.get_data()[0]
    qy = q.get_data()[1]
    pxnext = p.next.get_data()[0]
    pynext = p.next.get_data()[1]
    qxnext = q.next.get_data()[0]
    qynext = q.next.get_data()[1]

    done = False

    while not done:
        done = True
        while True:
            temp_slope = get_slope(px, qx, py, qy)  # get slope of temp line
            l_slope = get_slope(pxnext, qx, pynext, qy)  # get slope of neighbor line
            if temp_slope > l_slope:
                r = p.next

                p = r
                px = p.get_data()[0]
                py = p.get_data()[1]
                pxnext = p.next.get_data()[0]
                pynext = p.next.get_data()[1]
                done = False
            else:
                break
        while True:
            temp_slope = get_slope(px, qx, py, qy)
            r_slope = get_slope(px, qxnext, py, qynext)
            if temp_slope > r_slope:
                r = q.next

                q = r
                qx = q.get_data()[0]
                qy = q.get_data()[1]
                qxnext = q.next.get_data()[0]
                qynext = q.next.get_data()[1]
                done = False
            else:
                break

    return p, q


def find_lower_tangent(l, r):
    p = l.head
    q = r.head
    px = p.get_data()[0]
    py = p.get_data()[1]
    qx = q.get_data()[0]
    qy = q.get_data()[1]
    pxnext = p.next.get_data()[0]
    pynext = p.next.get_data()[1]
    qxnext = q.next.get_data()[0]
    qynext = q.next.get_data()[1]

    done = False

    while not done:
        done = True
        while True:
            temp_slope = get_slope(px, qx, py, qy)  # get slope of temp line
            l_slope = get_slope(pxnext, qx, pynext, qy)  # get slope of neighbor line
            if temp_slope > l_slope:
                r = p.prev

                p = r
                px = p.get_data()[0]
                py = p.get_data()[1]
                pxnext = p.next.get_data()[0]
                pynext = p.next.get_data()[1]

                done = False
            else:
                break
        while True:
            temp_slope = get_slope(px, qx, py, qy)
            r_slope = get_slope(px, qxnext, py, qynext)
            if temp_slope > r_slope:
                r = q.prev
                q = r
                qx = q.get_data()[0]
                qy = q.get_data()[1]
                qxnext = q.next.get_data()[0]
                qynext = q.next.get_data()[1]
                done = False
            else:
                break
    return p, q


def merge(l, r):
    p, q = find_upper_tangent(l, r)
    top_left, top_right = find_lower_tangent(l, r)
    p.next = q
    q.prev = p
    top_left.next = top_right
    top_right.prev = top_left
    hull = LinkedList(l.tail, r.head)
    return hull


def recursive_helper(points):
    if len(points) < 2:
        node = Node(points[0])
        node.next = node
        node.prev = node
        return LinkedList(node, node)
    mid = len(points) // 2
    L = recursive_helper(points[:mid])
    R = recursive_helper(points[mid:])
    H = merge(L, R)

    return H


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    sorted_points = sorted(points, key=x_coord)
    H = recursive_helper(sorted_points)
    lst = []
    H_size = count_nodes(H.head)
    for i in range(H_size):
        head = H.head
        tup = (head.get_data()[0], head.get_data()[1])
        lst.append(tup)
        H.head = H.head.next

    return lst
