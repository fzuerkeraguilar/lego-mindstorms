from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode


class PointFinder(Mode):
    INITIAL_SPEED = 100
    INITIAL_SIDE_LENGTH = 1000

    def __init__(self, color_sensor, distance_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)

    def circle_search(self):
        red_found = False
        white_found = False
        distance = 960

        for i in range(0, 3):
            while self.drivebase.distance() > distance:
                self.drivebase.drive(self.INITIAL_SPEED, 0)
                color = self.color_sensor.color()
                if not red_found and color == Color.RED:
                    red_found = True
                    self.hub.speaker.beep()
                if not white_found and color == Color.WHITE:
                    white_found = True
                    self.hub.speaker.beep()
                if red_found and white_found:
                    self.drivebase.stop()
                    return
            self.drivebase.stop()
            self.drivebase.turn(-90)
            self.drivebase.reset()

        while stop_distance > 500:
            stop_distance -= 70
            for i in range(0, 4):
                while self.drivebase.distance() < distance:
                    self.drivebase.drive(self.INITIAL_SPEED, 0)
                    rgb = self.color_sensor.rgb()
                    if rgb[0] > 50 and not red_found:
                        red_found = True
                        self.hub.speaker.beep()
                        if red_found and white_found:
                            self.drivebase.stop()
                            return
                    if rgb[0] > 50 and rgb[1] > 50 and rgb[2] > 50 and not white_found:
                        white_found = True
                        self.hub.speaker.beep()
                        if red_found and white_found:
                            self.drivebase.stop()
                            return
                self.drivebase.stop()
                self.drivebase.turn(-90)
                self.drivebase.reset()

    def run(self):
        self.circle_search()
