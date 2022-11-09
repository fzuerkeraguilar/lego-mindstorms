from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode
from pybricks.tools import wait

class BoxPusher(Mode):
    INITIAL_SPEED = 50
    DISTANCE_BIAS = 3
    THRESHOLD_DISTANCE = 20
    LEFT = -90
    CENTER = 0
    RIGHT = 90

    def __init__(self, ev3_hub, drivebase,
    color_sensor, distance_sensor, touch_sensor, right_motor, left_motor, speed=self.INITIAL_SPEED):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)
        self.left_motor = left_motor
        self.right_motor = right_motor

    def run(self):
        self.find_start_pos()
        self.push_box()
        self.find_end_pos()

    def find_start_pos(self):
        self.distance_sensor.measure_angle(this.LEFT)
        self.drive_guided_straight(50)

    def push_box(self):
        # find the box
        self.distance_sensor.measure_angle(this.RIGHT)
        self.drive_until_box_found(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.turn(90)

        # push box until leaving the box's field
        self.drive_until_line() # ignore first white line
        self.drive_until_line()
        self.drivebase.straight(-50)
        self.drivebase.turn(90)

        # drive behind the box
        self.distance_sensor.measure_angle(this.LEFT)
        self.drive_until_box_lost(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.turn(-90)

        self.drive_until_box_found(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.straight(20)
        self.drivebase.turn(-90)
        
        # push box into target field
        self.drive_until_line()


    def find_end_pos(self):
        self.drivebase.straight(-50)
        self.drivebase.turn(-90)
        self.drive_until_line()
        self.drivebase.turn(-90)
        self.distance_sensor.measure_angle(this.LEFT)
        self.drive_guided_straight(60)
        
    def drive_guided_straight(self, run_cycles, speed = self.INITIAL_SPEED, bias = self.DISTANCE_BIAS):
        "Drive straight for run_cycles with guidance from the distance sensor"
        self.drivebase.stop()
        wall_distance = self.distance_sensor.distance()
        left_speed = speed
        right_speed = speed
        cycle = 0
        
        while cycle < run_cycles:
            self.left_motor.run(speed)
            self.right_motor.run(speed)

            current_distance = self.distance_sensor.read()
            if (current_distance > wall_distance + bias):
                # steer left
                left_speed = speed - 3
                right_speed = speed
            elif (current_distance < wall_distance - bias):
                # steer right
                left_speed = speed
                right_speed = speed - 3
            else:
                # steer clear
                left_speed = speed
                right_speed = speed
            
            cycle = cycle + 1
            wait(10)

        self.left_motor.stop()
        self.right_motor.stop()

    def drive_until_line(self):
        # while self.color_sensor.color() != Color.WHITE
            # drive

    def drive_until_threshold_met(self, threshold_distance, speed, overshoot_time):
        "Drive forward until an object at threshold_distance is detected. Then keep driving for overshoot_time."
        "Positive threshold to detect objects entering the view, negative for objects leaving."
        if self.distance_sensor.distance() - threshold_distance < 0:
            return

        self.drivebase.stop()
        self.right_motor.run(speed)
        self.left_motor.run_time(speed)

        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.distance_sensor.distance() - threshold_distance < 0:
                # keep driving for overshoot_time. wait is true to avoid a next loop iteration
                self.right_motor.run_time(speed, overshoot_time, then=Stop.BRAKE, wait=True)
                self.left_motor.run_time(speed, overshoot_time, then=Stop.BRAKE, wait=True)
                return


    def drive_until_box_found(self, threshold_distance, speed = self.INITIAL_SPEED, overshoot_time = 0):
        "Drive forward until an object nearer than threshold_distance is detected. Then keep driving for overshoot_time"
        self.drive_until_threshold_met(self, threshold_distance, speed, overshoot_time)
        

    def drive_until_box_lost(self, threshold_distance, speed = self.INITIAL_SPEED, overshoot_time = 0):
        "Drive forward until an object nearer than threshold_distance is not detected anymore. Then keep driving for overshoot_time"
        self.drive_until_threshold_met(self, -threshold_distance, speed, overshoot_time)