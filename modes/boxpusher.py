from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode


class BoxPusher(Mode):
    INITIAL_SPEED = 50

    def __init__(self, ev3_hub, drivebase,
    color_sensor, distance_sensor, touch_sensor, speed=self.INITIAL_SPEED):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)

    def run():
        self.find_start_pos()
        self.push_box()
        self.find_end_pos()

    def find_start_pos():
        self.distance_sensor.measure_angle(Position.LEFT)
        self.drive_guided_straight()

    def push_box():
        self.distance_sensor.measure_angle(Position.RIGHT)
        self.drive_until_box_found()
        self.drivebase.turn(90)

        self.drive_until_line() # ignore first line
        self.drive_until_line()
        self.drivebase.straight(-50)
        self.drivebase.turn(90)

        self.distance_sensor.measure_angle(Position.LEFT)
        self.drive_until_box_lost()
        self.drivebase.turn(-90)

        self.drive_until_box_found()
        self.drivebase.straight(20)
        self.drivebase.turn(-90)
        
        self.drive_until_line()


    def find_end_pos():
        self.drivebase.straight(-50)
        self.drivebase.turn(-90)
        self.drive_until_line()
        self.drivebase.turn(-90)
        self.distance_sensor.measure_angle(Position.LEFT)
        self.drive_guided_straight()
        
    def drive_guided_straight():
        wall_distance = self.distance_sensor.distance()
        # while drive
            # if (wall_distance < distance_sensor.read() - bias):
                # steer left
            # elif (wall_distance > distance_sensor.read() + bias):
                # steer right

    def drive_until_line():
        # while self.color_sensor.color() != Color.WHITE
            # drive

    def drive_until_box_found():
        wall_distance = self.distance_sensor.distance()
        # while !(distance_sensor.read() < wall_distance - bias)
            # drive

    def drive_until_box_lost():
        box_distance = self.distance_sensor.distance()
        # while (distance_sensor.read() > box_distance + bias)
            # drive