from .entity import Agent
from .utils.geometry import *

import numpy as np


class SocialForceAgent(Agent):
    def __init__(self, x, y, width, height, vel=(0, 0), shape="circle", color="blue"):
        super().__init__(x, y, width, height, vel, shape, color)
        self.waypoints = []

    def add_waypoint(self, goal_pos):
        self.waypoints.append(goal_pos)

    def step(self, get_obstacles, get_neighbors):
        if len(self.waypoints) == 0:
            return 0, 0
        if dist((self.x, self.y), self.waypoints[0]) < .25:
            if len(self.waypoints) > 1:
                self.waypoints = self.waypoints[1:]
            else:
                return 0, 0

        cur_vel = np.array(self.vel, dtype="float64")
        cur_pos = np.array([self.x, self.y])

        goal = self.waypoints[0]
        goal_angle = np.arctan2(goal[1] - self.y, goal[0] - self.x)
        goal_force = 1.3 * np.array([np.cos(goal_angle), np.sin(goal_angle)]) - cur_vel

        social_force = np.array([0., 0.])
        neighbors = list(get_neighbors(10))
        for neighbor in neighbors:
            d = neighbor[0]
            a = neighbor[1]
            i = np.arctan2(self.vel[1], self.vel[0])

            theta = np.arctan2(np.sin(a-i), np.cos(a-i))
            d_vec = np.array([np.cos(a), np.sin(a)])
            Vab = 3. * np.exp(-d / .2)
            social_force += d_vec * Vab

        obstacle_force = np.array([0., 0.])
        obstacles = list(get_obstacles(1))
        for obstacle in obstacles:
            d = obstacle[0]
            a = obstacle[1]
            d_vec = np.array([np.cos(a), np.sin(a)])
            Uab = 3. * np.exp(-d / .2)
            obstacle_force += d_vec * Uab

        delta_time = .2
        vel_max = 1.3
        forces = goal_force + obstacle_force + social_force
        cur_vel += delta_time * forces
        if np.linalg.norm(cur_vel) > vel_max:
            cur_vel = cur_vel / np.linalg.norm(cur_vel) * vel_max
        cur_vel *= delta_time
        return cur_vel[0], cur_vel[1]
