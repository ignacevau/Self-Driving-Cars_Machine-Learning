import pygame
import math
import data as d
import json


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, r):
        return Vector2(self.x * r, self.y * r)

    def __truediv__(self, r):
        return Vector2(self.x / r, self.y / r)

    def rotated(self, angle):
        angle *= math.pi / 180
        return Vector2(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.y * math.cos(angle) - self.x * math.sin(angle)
        )

    def rotate(self, angle):
        angle *= math.pi / 180
        x = self.x
        y = self.y
        cos = math.cos(angle)
        sin = math.sin(angle)
        self.x = x * cos + y * sin
        self.y = y * cos - x * sin

    def tupled(self):
        return (self.x, self.y)

class Algs:
    def __init__(self):
        pass

    @classmethod
    def get_segment_inters(self, p1, p2, p3, p4):
        d13 = p1 - p3
        d34 = p3 - p4
        d12 = p1 - p2
        d21 = p2 - p1

        n1 = (d12.x*d34.y - d12.y*d34.x)
        n2 = (d12.x*d34.y - d12.y*d34.x)

        # Segments are parallel
        if n1 == 0 or n2 == 0:
            return None

        t = (d13.x*d34.y - d13.y*d34.x) / n1
        u = -(d12.x*d13.y - d12.y*d13.x) / n2

        if t < 0 or t > 1 or u < 0 or u > 1:
            return None
        return Vector2(int(p1.x + t*d21.x), int(p1.y + t*d21.y))

    @classmethod
    def check_segment_inters(self, p1, p2, p3, p4):
        d13 = p1 - p3
        d34 = p3 - p4
        d12 = p1 - p2

        n1 = (d12.x*d34.y - d12.y*d34.x)
        n2 = (d12.x*d34.y - d12.y*d34.x)

        # Segments are parallel
        if n1 == 0 or n2 == 0:
            return False

        t = (d13.x*d34.y - d13.y*d34.x) / n1
        u = -(d12.x*d13.y - d12.y*d13.x) / n2

        if t < 0 or t > 1 or u < 0 or u > 1:
            return False
        return True

    @classmethod
    def get_distance(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.sqrt(dx*dx + dy*dy)

class Import:
    def __init__(self):
        pass

    @classmethod
    def import_json_track(self, track_name):
        with open(track_name) as data_file:    
            track_data = json.load(data_file)
            d.WALL_IN = d.WALL_I_EXT = track_data["points1"]
            d.WALL_OUT = d.WALL_O_EXT = track_data["points2"]
            d.CHECKPOINTS = track_data["checkPoints"]
            d.START_POSITION = (track_data["startPoint"][0], track_data["startPoint"][1])
            d.active_checkp = d.CHECKPOINTS[:]
            d.WALL_I_EXT.append(d.WALL_IN[0])
            d.WALL_O_EXT.append(d.WALL_OUT[0])

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sum_matrix_float(v, r):
    a = [None]*len(v)
    for i in range(len(v)):
        a[i] = v[i] + r
    return a

def clamp(min, max, value):
    if value < min:
        return min
    elif value > max:
        return max
    return value