from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from pybricks.tools import wait

import random


class PointFinder(Mode):
    INITIAL_SPEED = 300
    INITIAL_SIDE_LENGTH = 1000
    red_found = False
    white_found = False

    def __init__(self, color_sensor, distance_sensor, touch_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sensor
        self.drivebase.reset()
        self.drivebase.settings(speed)
        self.red_found = False
        self.white_found = False

    def circle_search(self):
        distances = []
        self.distance_sensor.set_up()

        self.drivebase.straight(50)
        self.drivebase.reset()
        for i in range(0, 2):
            while not self.touch_sensor.pressed():
                self.drive_guided_straight(35)
                if self.check_color():
                    return
            self.drivebase.stop()
            distance = self.drivebase.distance()
            self.hub.screen.print("Distance: ", distance)
            distances.append(distance)
            self.drivebase.straight(-30)
            self.drivebase.turn(-90)
            self.drivebase.reset()

        distances[0] -= 100
        distances[1] -= 50

        while distances[0] > 0 and distances[1] > 0:
            for i in range(0, 2):
                wall_distance = self.distance_sensor.distance()
                while self.drivebase.distance() < distances[i] and not self.touch_sensor.pressed():
                    self.drive_guided_straight(wall_distance)
                    if self.check_color():
                        return
                self.drivebase.stop()
                if self.touch_sensor.pressed():
                    distances[i] = self.drivebase.distance()
                    self.drivebase.straight(-30)
                distances[i] -= 50
                self.drivebase.turn(-90)
                self.drivebase.reset()

    def drive_guided_straight(self, wall_distance_mm):
        current_distance = self.distance_sensor.distance()
        if current_distance < wall_distance_mm:
            self.drivebase.drive(self.INITIAL_SPEED, -3)
        else:
            self.drivebase.drive(self.INITIAL_SPEED, 3)
    
    def spiral_search(self):
        self.drivebase.reset()
        length = 0
        while not self.touch_sensor.pressed():
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        length = self.drivebase.distance()
        self.drivebase.straight(-20)
        self.drivebase.turn(-90)
        self.drivebase.reset()
        width = 0
        while not self.touch_sensor.pressed():
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        width = self.drivebase.distance()
        self.drivebase.straight(-20)
        self.drivebase.turn(-90)
        self.drivebase.reset()
        while self.drivebase.distance() < length:
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        self.drivebase.straight(-20)
        self.drivebase.turn(-90)
        self.drivebase.reset()
        while self.drivebase.distance() < width:
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        self.drivebase.straight(-20)
        self.drivebase.turn(-90)
        self.drivebase.reset()
        while self.drivebase.distance() < length / 2:
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        self.drivebase.turn(-90)
        self.drivebase.reset()
        while self.drivebase.distance() < width / 2:
            self.drivebase.drive(self.INITIAL_SPEED, 0)
            if self.check_color():
                return
        self.drivebase.stop()
        # Drive spirally until both colors are found or wall is hit
        # Decrease turn_rate by 1 every 10 cm
        while True:
            turn_rate = 90
            self.drivebase.drive(self.INITIAL_SPEED, turn_rate)
            if self.check_color():
                return
            if self.drivebase.distance() % 10 == 0:
                turn_rate -= 1
                self.hub.screen.print("Turn rate: ", turn_rate)
            
            

    def check_color(self):
        color = self.color_sensor.color()
        if not self.red_found and color == Color.RED:
            self.red_found = True
            self.hub.speaker.beep()
            self.hub.screen.print("Found red!")
        if not self.white_found and color == Color.WHITE:
            self.white_found = True
            self.hub.speaker.beep()
            self.hub.screen.print("Found white!")
        if self.red_found and self.white_found:
            self.hub.speaker.beep()
            self.hub.screen.print("Found both!")
            self.drivebase.stop()
            return True
        return False

    def run(self):
        self.circle_search()

    def random_search(self):
        self.drivebase.drive(self.INITIAL_SPEED, 0)

        while True:
            color_found = self.color_sensor.color()
            self.hub.screen.print("Color: ", color_found)
            self.check_collision_or_blue_line_and_turn(color_found)
            if self.check_colors(color_found):
                self.drivebase.stop()
                return

    def check_collision_or_blue_line_and_turn(self, color_found):
        if self.touch_sensor.pressed() or color_found == Color.BLUE:
            self.drivebase.stop()
            random_turn = random.randint(-80, 80)
            self.drivebase.straight(-50)
            self.drivebase.turn(random_turn + 180)
            self.drivebase.drive(self.INITIAL_SPEED, 0)

    def check_colors(self, color_found):
        if color_found == Color.RED and not self.red_color_found:
            self.red_color_found = True
            self.hub.speaker.beep()
        elif color_found == Color.WHITE and not self.white_color_found:
            self.white_color_found = True
            self.hub.speaker.beep()
        return self.red_color_found and self.white_color_found
