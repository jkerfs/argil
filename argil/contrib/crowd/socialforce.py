from argil.entity import Agent, Entity
from argil.utils.geometry import *

import numpy as np


class SocialForceAgent(Agent):
    def __init__(self, x, y, radius, vel=(0, 0), vel_max=1.3, color="blue"):
        #super(Agent, self).__init__(self.step, x=x, y=y, radius=radius)
        self.params = {"x": x, "y": y, "radius": radius}
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.color = color
        self.waypoints = []
        self.vel_max = vel_max
        self.done = False

    def add_waypoint(self, goal_pos):
        self.waypoints.append(goal_pos)

    def step(self, this, get_obstacles, get_neighbors):
        if self.done:
            return True
        if len(self.waypoints) == 0:
            self.done = True
            return True
        if dist((self.x, self.y), self.waypoints[0]) < .1:
            if len(self.waypoints) > 1:
                self.waypoints = self.waypoints[1:]
            else:
                self.x = self.waypoints[-1][0]
                self.y = self.waypoints[-1][1]
                self.done = True
                return True


        delta_time = .05
        mass = 80

        cur_vel = np.array(self.vel, dtype="float64")
        cur_pos = np.array([self.x, self.y])

        goal = self.waypoints[0]
        goal_angle = np.arctan2(goal[1] - self.y, goal[0] - self.x)
        goal_force = (np.array([np.cos(goal_angle), np.sin(goal_angle)]) - cur_vel) * mass / delta_time

        social_force = self.get_agent_force(cur_pos, cur_vel, get_neighbors(10))
        obstacle_force = self.get_obstacle_force(get_obstacles(10))

        force = goal_force + obstacle_force + social_force
        cur_vel += delta_time * force / mass
        if np.linalg.norm(cur_vel) > self.vel_max:
            cur_vel = cur_vel / np.linalg.norm(cur_vel) * self.vel_max
        cur_vel *= delta_time
        self.x += cur_vel[0]
        self.y += cur_vel[1]

        return False

    def get_agent_force(self, cur_pos, cur_vel, neighbors):
        BODY_FORCE = 1200
        FRICTION = 2400
        FORCE_DISTANCE = .015
        social_force = np.array([0., 0.])
        for neighbor in neighbors:
            d = neighbor[0]
            a = neighbor[1]
            n_pos = (neighbor[2].x, neighbor[2].y)
            normal_ij = (cur_pos - n_pos) / d
            distance_ij = neighbor[0]
            radii_ij = neighbor[2].radius + self.radius
            mag = 2000 * np.exp((radii_ij - distance_ij) / FORCE_DISTANCE)
            force = mag * normal_ij
            if distance_ij < radii_ij:
                tangent_ij = np.array([normal_ij[0], normal_ij[1]])
                f_pushing = normal_ij * BODY_FORCE * (radii_ij - distance_ij)
                f_friction = normal_ij * FRICTION * (radii_ij - distance_ij) * abs(neighbor[2].vel - cur_vel) * tangent_ij
                force += f_pushing + f_friction
            social_force += force
        return social_force

    def get_obstacle_force(self, obstacles):
        obstacle_force = np.array([0., 0.])
        for obstacle in obstacles:
            d = obstacle[0]
            a = obstacle[1]
            d_vec = np.array([np.cos(a), np.sin(a)])
            mag = 4000 * np.exp((self.radius - d) / .015)
            obstacle_force += d_vec * mag

        return obstacle_force

    def init_view(self):
        return "circle", {"color": self.color, "radius": self.radius}

    def render_view(self):
        return {
            "x": self.x,
            "y": self.y,
        }


