import math
import numpy as np

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def intersect(r1, r2):
    x1, y1, x1b, y1b = r1.x, r1.y, r1.x + r1.width, r1.y + r1.height
    x2, y2, x2b, y2b = r2.x, r2.y, r2.x + r2.width, r2.y + r2.height
    res = not ((x1b < x2 or x2b < x1) or (y2b < y1 or y1b < y2))
    return res


def rect_distance(p, r):
    px, py = p.x, p.y
    rx, ry, rw, rh = r.x, r.y, r.width, r.height
    dx = np.array([rx - px, 0, px - (rx + rw)])
    dy = np.array([ry - py, 0, py - (ry + rh)])

    dx = max(dx) if np.argmax(dx) == 2 else -max(dx)
    dy = max(dy) if np.argmax(dy) == 2 else -max(dy)
    return np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx)


def circle_distance(p, c):
    return dist((p.x, p.y), (c.x, c.y)), np.arctan2(c.y - p.y, c.x - p.x)