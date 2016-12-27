import numpy as np
from pygame import Rect

def reconstruct_path(last, came_from):
    total_path = [last]
    while last in came_from.keys():
        last = came_from[last]
        total_path.append(last)
    return total_path


def euclidean_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def neighbors(pos, width, height):
    for step in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nxt = (pos[0] + step[0], pos[1] + step[1])
        if nxt[0] >= 0 and nxt[0] < width and nxt[1] >= 0 and nxt[1] < height:
            yield nxt


def a_star(start, goal, width, height, obstacles):
    x, y = start
    closed_set = set()
    open_set = set()
    open_set.add(start)
    came_from = {}

    g_score = np.empty((width, height))
    g_score[:] = np.Inf
    g_score[x, y] = 0
    f_score = np.empty((width, height))
    f_score[:] = np.Inf
    f_score[x, y] = euclidean_dist(start, goal)

    while open_set:
        lowest_fscore = np.Inf
        current = None
        for n in open_set:
            if f_score[n[0], n[1]] < lowest_fscore:
                lowest_fscore = f_score[n[0], n[1]]
                current = n
        if current[0] == goal[0] and current[1] == goal[1]:
            return reconstruct_path(current, came_from)
        open_set.remove(current)
        closed_set.add(current)
        for neighbor in neighbors(current, width, height):

            if neighbor in closed_set or Rect(neighbor[0], neighbor[1], 1, 1).collidelist(obstacles):
                continue
            tenative_g_score = g_score[current[0], current[1]] + euclidean_dist(current, neighbor)
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tenative_g_score >= g_score[neighbor[0], neighbor[1]]:
                continue
            came_from[neighbor] = current
            g_score[neighbor] = tenative_g_score
            f_score[neighbor] = g_score[neighbor] + euclidean_dist(neighbor, goal)
    return None
