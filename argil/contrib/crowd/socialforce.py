from argil.entity import Agent
from argil.utils.geometry import *

import numpy as np


class SocialForceConstants:
    def __init__(self, body_force=1200, friction=2400, social_distance=.3, social_force=2000, obstacle_force=4000,
                 obstacle_distance=.015):
        self.body_force = body_force
        self.friction = friction

        self.social_distance = social_distance
        self.social_force = social_force

        self.obstacle_distance = obstacle_distance
        self.obstacle_force = obstacle_force



class SocialForceAgent(Agent):
    def __init__(self, x, y, radius, vel=(0, 0), vel_max=1.3, color="blue", delay=None, constants=None):
        Agent.__init__(self)
        self.params = {"x": x, "y": y, "radius": radius, "waypoints": [],
                       "vel": vel, "vel_max": vel_max, "color": color, "delay": delay,
                       "start_x": x, "start_y": y}
        if not constants:
            self.constants = SocialForceConstants()
        else:
            self.constants = constants
        self.priority = np.random.rand()

        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.color = color
        self.waypoints = []
        self.vel_max = vel_max
        self.vel_des = .8 * vel_max
        self.done = False
        self.delay = delay
        if self.delay is not None:
            self.start_x = x
            self.start_y = y
            self.x = np.inf
            self.y = np.inf
        self.preferred = np.array([0., 0.])

    def add_waypoint(self, goal_pos):
        self.waypoints.append(goal_pos)
        self.params["waypoints"].append(goal_pos)

    def step(self, this, get_obstacles, get_neighbors):
        if type(self.delay) == int:
            self.delay -= 1
            if self.delay > 0:
                self.x = np.inf
                self.y = np.inf
                return False
            else:
                self.x = self.start_x
                self.y = self.start_y
                self.delay = None

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
        self.preferred = np.array([np.cos(goal_angle), np.sin(goal_angle)])
        goal_force = (self.preferred - cur_vel) * mass / delta_time

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
        social_force = np.array([0., 0.])

        for neighbor in neighbors:
            d = neighbor[0]
            a = neighbor[1]
            n = neighbor[2]
            #if n.done:
            #    continue

            right_of_way = self.priority > n.priority

            n_pos = (n.x, n.y)
            normal_ij = (cur_pos - n_pos) / d
            distance_ij = neighbor[0]
            radii_ij = self.radius - n.radius

            d_agt = self.constants.social_distance

            avoid_norm = np.array(normal_ij)
            if not right_of_way:
                d_agt = self.constants.social_distance + n.radius * .5

                prefSpeed = n.vel_des
                if prefSpeed < .0001:
                    perpDir = (-normal_ij[1], normal_ij[0])
                else:
                    prefDir = n.preferred
                    perpDir = (-prefDir[1], prefDir[0])
                avoid_norm = perpDir

            mag = self.constants.social_force * np.exp((radii_ij - distance_ij) / d_agt)
            force = np.array(mag) * np.array(avoid_norm)

            if distance_ij < radii_ij:
                tangent_ij = np.array([normal_ij[0], normal_ij[1]])
                f_pushing = normal_ij * self.constants.body_force * (radii_ij - distance_ij)
                f_friction = normal_ij * self.constants.friction * (radii_ij - distance_ij) * abs(n.vel - cur_vel) * tangent_ij
                force += f_pushing + f_friction
            social_force += force
        return social_force

    def get_obstacle_force(self, obstacles):
        obstacle_force = np.array([0., 0.])
        for obstacle in obstacles:
            d = obstacle[0]
            a = obstacle[1]
            d_vec = np.array([np.cos(a), np.sin(a)])
            mag = self.constants.obstacle_force * np.exp((self.radius - d) / self.constants.obstacle_distance)
            obstacle_force += d_vec * mag

        return obstacle_force

    def reset(self):
        Agent.__init__(self)
        self.done = False
        if self.delay is not None:
            self.start_x = self.x
            self.start_y = self.y
            self.x = np.inf
            self.y = np.inf
        self.preferred = np.array([0., 0.])
