import math
import numpy as np

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def intersect(r1, r2):
    x1, y1, x1b, y1b = r1.x, r1.y, r1.x + r1.width, r1.y + r1.height
    x2, y2, x2b, y2b = r2.x, r2.y, r2.x + r2.width, r2.y + r2.height
    res = not ((x1b < x2 or x2b < x1) or (y2b < y1 or y1b < y2))
    return res


def rect_distance(r1, r2):
    if intersect(r1, r2):
        return 0, 0

    x1, y1, x1b, y1b = r1.x, r1.y, r1.x + r1.width, r1.y + r1.height
    x2, y2, x2b, y2b = r2.x, r2.y, r2.x + r2.width, r2.y + r2.height

    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist((x1, y1b), (x2b, y2)), np.arctan2(y1b - y2, x1 - x2b)
    elif left and bottom:
        return dist((x1, y1), (x2b, y2b)), np.arctan2(y1 - y2b, x1 - x2b)
    elif bottom and right:
        return dist((x1b, y1), (x2, y2b)), np.arctan2(y1 - y2b, x1b - x2)
    elif right and top:
        return dist((x1b, y1b), (x2, y2)), np.arctan2(y1b - y2, x1b - x2)
    elif left:
        return x1 - x2b, np.arctan2(0, x1 - x2b)
    elif right:
        return x2 - x1b, np.arctan2(0, x1b - x2)
    elif bottom:
        return y1 - y2b, np.arctan2(y1 - y2b, 0)
    elif top:
        return y2 - y1b, np.arctan2(y1b - y2, 0)