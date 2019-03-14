import pygame as pg
from utility import Vector2, Algs
import data as d
from neural_net import NeuralNetWork
import main
import copy
import math

class Car:
    """ Class of a car that drives the track """
    def __init__(self, net=None):
        self.position = Vector2(d.START_POSITION[0], d.START_POSITION[1])
        self.rotation = 0
        self.direction = Vector2(1, 0)
        self.direction_normal = Vector2(0, 1)
        self.frame = [Vector2()] * 4
        self.sensors = [Sensor((180 / (d.SENSOR_COUNT-1)) * i - 90) for i in range(d.SENSOR_COUNT)]
        self.dead = False
        self.turn = 0.5
        if net == None:
            self.neural_net = NeuralNetWork(d.SENSOR_COUNT, d.HIDDEN_LAYERS, 1)
        else:
            self.neural_net = net


    def move(self):
        """ Update the car's position """
        self.position += self.direction * d.VELOCITY

        # < 0.5 = left and > 0.5 = right 
        # self.turn is always between 0 and 1
        self.rotate(self.turn - 0.5)


    def rotate(self, angle):
        """ Rotate the car over a given angle (degrees) """
        self.rotation = (self.rotation + angle * d.TURN_SPEED)
        self.direction.rotate(angle * d.TURN_SPEED)


    def draw(self):
        """ Draw the car and its sensors """
        color = d.GRAY
        if d.best_car == self:
            # This car is currently the furthest
            color = d.WHITE

        # Draw the frame of the car
        car_frame = [self.frame[i].tupled() for i in range(len(self.frame))]
        pg.draw.lines(d.SURFACE, color,True, car_frame, 2)

        # Draw the sensors of the car
        if not self.dead:
            self.draw_sensors()


    def draw_sensors(self):
        """ Draw the car its sensors """
        pass
        color = d.DARK_GREEN
        width = 1

        if d.best_car == self:
            # This car is currently the furthest
            color = d.GREEN
            width = 2

        # Draw every sensor
        for sensor in self.sensors:
            sensor.draw(color, width)


    def update(self):
        """ Update the car object """
        self.direction_normal = self.direction.rotated(90)
        self.update_frame()
        self.update_sensors()
        self.check_wall_col()
        self.check_checkpoint_col()
        self.turn = self.neural_net.forward_prop([self.sensors[i].length for i in range(d.SENSOR_COUNT)])
        self.check_crazy_rotation()
        self.move()


    def check_crazy_rotation(self):
        """ Check whether the car is stuck in an infinite loop """
        if math.fabs(self.rotation) > d.ROTATION_THRESHOLD:
            self.die()


    def update_sensors(self):
        """ Update every sensor of the car """
        for sensor in self.sensors:
            sensor.update(self.direction, self.position)


    def update_frame(self):
        """ Calculate the positions of the points of the car's frame """
        y = self.direction * d.CAR_HEIGHT / 2
        x = self.direction_normal * d.CAR_WIDTH / 2
        pos = self.position
        # back-left
        self.frame[0] = (pos - y - x)
        # front-left
        self.frame[1] = (pos + y - x)
        # front-right
        self.frame[2] = (pos + y + x)
        # back-right
        self.frame[3] = (pos - y + x)


    def check_checkpoint_col(self):
        """ Check whether the car collects a checkpoint """

        # First point of the first active checkpoint
        p1 = Vector2(d.active_checkp[0][0][0], d.active_checkp[0][0][1])
        # Second point of the first active checkpoint
        p2 = Vector2(d.active_checkp[0][1][0], d.active_checkp[0][1][1])

        if self.check_col(p1, p2):
            # Check for collision with the checkpoint
            d.active_checkp.pop(0)
            d.best_car = self

            if len(d.active_checkp) == 0:
                self.restart_simulation()


    def check_wall_col(self):
        """ Check whether the car collides with a wall """

        # Check collision with inner wall
        for i in range(len(d.WALL_I_EXT)-1):
            w_p1 = d.WALL_I_EXT[i]
            w_p2 = d.WALL_I_EXT[i+1]
            p1 = Vector2(w_p1[0], w_p1[1])
            p2 = Vector2(w_p2[0], w_p2[1])

            if self.check_col(p1, p2):
                self.die()

        # Check collision with outer wall
        for i in range(len(d.WALL_O_EXT)-1):
            w_p1 = d.WALL_O_EXT[i]
            w_p2 = d.WALL_O_EXT[i+1]
            p1 = Vector2(w_p1[0], w_p1[1])
            p2 = Vector2(w_p2[0], w_p2[1])

            if self.check_col(p1, p2):
                self.die()


    def die(self):
        """ Kill the car """
        if self.dead:
            return
        self.dead = True

        if len(d.shitty_cars) < d.SHITTY_CAR_COUNT:
            # Car died early
            d.shitty_cars.append(self)
        if d.active_car_count < d.FIT_CARS_COUNT:
            # Car died as one of the last
            d.fittest_cars.append(self)
            
        d.active_car_count -= 1

        # Update the information text
        d.TXT_ALIVE = "Cars alive : %s" %str(d.active_car_count)
        d.TXT_DEAD = "Cars dead : %s" %str(d.POPULATION_COUNT - d.active_car_count)

        if(d.active_car_count == 0):
            # This was the last car
            self.restart_simulation()


    def check_col(self, p1, p2):
        """ Check whether car collides with a given segment """
        for i in range(len(self.frame)-1):
            # Does not check for the back of the car
            p3 = self.frame[i]
            p4 = self.frame[i+1]

            inters = Algs.check_segment_inters(p1, p2, p3, p4)
            if inters:
                return True
        return False


    def restart_simulation(self):
        """ Restart the simulation """
        main.draw_text()
        # Wait a second
        pg.time.wait(int(d.RESTART_WAIT_TIME*1000))

        main.reload()


class Sensor:
    """ Sensor with which the player sees in a locked direction\n
        Parameters: \n
        \tangle = Angle of the sensor in respect to the player (degrees)"""
    def __init__(self, angle):
        self.angle = angle
        self.dir = Vector2()
        self.pos = Vector2()
        self.end_pos = Vector2()
        self.car_dir = Vector2()
        self.inters = None
        self.length = d.SENSOR_LENGTH


    def update(self, car_dir, car_pos):
        """ Update the sensor\n
            Parameters:
            \tship_dir = direction vector of the ship
            \tship_pos = position vector of the ship """
        self.get_wall_collision()
        self.car_dir = car_dir
        self.dir = car_dir.rotated(self.angle)
        self.pos = car_pos + self.car_dir * d.CAR_HEIGHT / 2
        self.update_length()


    def update_length(self):
        if self.inters != None:
            self.end_pos = self.inters
        else:
            self.end_pos = self.pos + self.dir * d.SENSOR_LENGTH

        self.length = Algs.get_distance(self.pos, self.end_pos)


    def draw(self, color, width):
        """ Draw the sensor """
        # There is an intersection
        if self.inters != None:
            # Draw the intersection point
            pg.draw.circle(d.SURFACE, color, self.inters.tupled(), 4)

        pg.draw.line(d.SURFACE, color, self.pos.tupled(), self.end_pos.tupled(), width)


    def get_wall_collision(self):
        """ Find intersection point with the wall """
        self.inters = None
        
        # Check collision with inner wall
        for i in range(len(d.WALL_IN)):
            if self.inters == None:
                j = 0 if len(d.WALL_IN)-1 == i else i + 1

                w_p1 = d.WALL_I_EXT[i]
                w_p2 = d.WALL_I_EXT[j]
                p1 = Vector2(w_p1[0], w_p1[1])
                p2 = Vector2(w_p2[0], w_p2[1])
                s = Algs.get_segment_inters(
                    p1, p2, self.pos, self.pos + self.dir * d.SENSOR_LENGTH)
                self.inters = s

        # Check collision with outer wall
        for i in range(len(d.WALL_O_EXT)-1):
            if self.inters == None:
                if i == len(d.WALL_IN)-1:
                    j = 0
                else:
                    j = i + 1
                    
                w_p1 = d.WALL_O_EXT[i]
                w_p2 = d.WALL_O_EXT[j]
                p1 = Vector2(w_p1[0], w_p1[1])
                p2 = Vector2(w_p2[0], w_p2[1])
                s = Algs.get_segment_inters(
                    p1, p2, self.pos, self.pos + self.dir * d.SENSOR_LENGTH)
                self.inters = s
