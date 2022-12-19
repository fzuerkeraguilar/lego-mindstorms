from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from pybricks.tools import wait


class PointFinder(Mode):
    INITIAL_SPEED = 150
    INITIAL_SIDE_LENGTH = 1000

    def __init__(self, color_sensor, distance_sensor, touch_sonsor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sonsor

    def circle_search(self):
        distances = []
        red_found = False
        white_found = False
        self.distance_sensor.set_up()

        for i in range(0, 2):
            while not self.touch_sensor.pressed():
                wall_distance = self.distance_sensor.distance()
                if wall_distance < 35:
                    self.drivebase.drive(self.INITIAL_SPEED, -3)
                else:
                    self.drivebase.drive(self.INITIAL_SPEED, 3)
                color = self.color_sensor.color()
                if not red_found and color == Color.RED and self.drivebase.distance() < 30:
                    red_found = True
                    self.screen.print("Found red!")
                    self.hub.speaker.beep()
                if not white_found and color == Color.WHITE:
                    white_found = True
                    self.screen.print("Found white!")
                    self.hub.speaker.beep()
                if red_found and white_found:
                    self.drivebase.stop()
                    return
            self.drivebase.stop()
            distance = self.drivebase.distance()
            self.hub.screen.print("Distance: ", distance)
            distances.append(distance)
            self.drivebase.straight(-30)
            self.drivebase.turn(-90)
            self.drivebase.reset()

        distances[0] -= 150
        distances[1] -= 50

        while distances[0] > 0 and distances[1] > 0:
            for i in range(0, 2):
                wall_distance = self.distance_sensor.distance()
                while self.drivebase.distance() < distances[i]:
                    if self.distance_sensor.distance() < wall_distance:
                        self.drivebase.drive(self.INITIAL_SPEED, -3)
                    else:
                        self.drivebase.drive(self.INITIAL_SPEED, 3)
                    color = self.color_sensor.color()
                    if not red_found and color == Color.RED:
                        red_found = True
                        self.hub.speaker.beep()
                        self.hub.screen.print("Found red!")
                    if not white_found and color == Color.WHITE:
                        white_found = True
                        self.hub.speaker.beep()
                        self.hub.screen.print("Found white!")
                    if red_found and white_found:
                        self.hub.speaker.beep()
                        self.hub.screen.print("Found both!")
                        self.drivebase.stop()
                        return
                distances[i] -= 50
                self.drivebase.turn(-90)
                self.drivebase.reset()

    def run(self):
        self.circle_search()
