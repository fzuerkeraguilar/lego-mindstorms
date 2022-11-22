from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode


class PointFinder(Mode):
    INITIAL_SPEED = 100
    INITIAL_SIDE_LENGTH = 1000

    def __init__(
        self, ev3_hub, drivebase, color_sensor, distance_sensor, speed=INITIAL_SPEED
    ):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)

    def circle_search(self):
        red_found = False
        white_found = False
        stop_distance = 40

        for i in range(0, 3):
            while self.distance_sensor.distance() > stop_distance:
                self.drivebase.drive(self.INITIAL_SPEED, 0)
                rgb = self.color_sensor.rgb()
                if rgb[0] > 10 and rgb[1] < 20 and rgb[2] < 20 and not red_found:
                    red_found = True
                    self.hub.speaker.beep()
                    if red_found and white_found:
                        self.drivebase.stop()
                        return
                if rgb[0] > 10 and rgb[1] > 40 and rgb[2] > 40 and not white_found:
                    white_found = True
                    self.hub.speaker.beep()
                    if red_found and white_found:
                        self.drivebase.stop()
                        return
            self.drivebase.turn(-87)

        while stop_distance < 500:
            stop_distance += 70
            for i in range(0, 4):
                while self.distance_sensor.distance() > stop_distance:
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
                self.drivebase.turn(-87)

    def run(self):
        self.circle_search()
