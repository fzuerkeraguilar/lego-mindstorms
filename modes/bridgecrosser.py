from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode
from controller.pcontroller import PController


class BridgeCrosser(Mode):

    RAMP_ANGLE = 15
    INITIAL_SPEED = 50
    WALL_DISTANCE = 572
    RAMP_LENGTH = 1050

    def __init__(self, color_sensor, distance_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.drivebase = config.get_drivebase(clean=True)

    def run(self):
        self.drive_up()
        return

        self.drivebase.straight(1050)
        self.drivebase.turn(-90)
        self.drivebase.straight(1260)
        self.drivebase.turn(-90)
        self.drivebase.straight(1000)

    def drive_up(self):
        self.distance_sensor.set_angle(-90)
        target_wall_distance = self.distance_sensor.distance()

        controller = PController(target_wall_distance, -0.1)
        speed = 50

        self.drivebase.reset()
        while self.drivebase.distance() < 600:
            # correct angle to drive straight
            current_wall_distance = self.distance_sensor.distance()
            turn_rate = min(controller.correction(current_wall_distance), 2)
            self.drivebase.drive(speed, turn_rate)
            self.hub.screen.print(turn_rate)

        while self.drivebase.distance() < 1050:
            pass

        self.drivebase.stop()

    def drive_down(self):
        self.drivebase.straight(1000)