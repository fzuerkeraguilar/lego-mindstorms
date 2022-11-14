from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor, GyroSensor
from modes.mode import Mode
from pybricks.tools import wait

class BoxPusher(Mode):
    WHITE = 42
    INITIAL_SPEED = 100
    CORRECTION_SPEED = 5
    DISTANCE_BIAS = 5
    THRESHOLD_DISTANCE = 20
    RIGHT = -90
    CENTER = 0
    LEFT = 90

    def __init__(self, ev3_hub, drivebase,
    color_sensor, distance_sensor, touch_sensor, right_motor, left_motor, speed=INITIAL_SPEED):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)
        self.left_motor = left_motor
        self.right_motor = right_motor

    def run(self):
        self.find_start_pos()
        self.push_box()
        self.find_end_pos()

    def find_start_pos(self):
        self.hub.screen.print("find start pos")
        self.hub.speaker.beep()
        self.drivebase.straight(50)
        self.distance_sensor.set_angle(self.LEFT)
        self.drive_guided_straight(10)

    def push_box(self):
        self.hub.screen.print("push box")
        self.hub.speaker.beep()
        # find the box
        self.distance_sensor.set_angle(self.RIGHT)
        self.drive_until_box_found(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.turn(90)

        # push box until leaving the box's field
        self.drive_until_line() # ignore first white line
        self.drive_until_line()
        self.drivebase.straight(-50)
        self.drivebase.turn(90)

        # drive behind the box
        self.distance_sensor.set_angle(self.LEFT)
        self.drive_until_box_lost(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.turn(-90)

        self.drive_until_box_found(self.THRESHOLD_DISTANCE, overshoot_time=20)
        self.drivebase.straight(20)
        self.drivebase.turn(-90)
        
        # push box into target field
        self.drive_until_line()


    def find_end_pos(self):
        self.hub.screen.print("find end pos")
        self.hub.speaker.beep()
        self.drivebase.straight(-50)
        self.drivebase.turn(-90)
        self.drive_until_line()
        self.drivebase.turn(-90)
        self.distance_sensor.set_angle(self.LEFT)
        self.drive_guided_straight(60)
        
    def drive_guided_straight(self, motor_cycles, speed = INITIAL_SPEED, bias = DISTANCE_BIAS):
        "Drive straight for motor_cycles with guidance from the distance sensor"
        self.hub.screen.print("guided straight")
        self.hub.speaker.beep()

        wall_distance = self.distance_sensor.distance()
        turn_rate = 0

        # use motor angle to detect driven length
        # self.left_motor.reset_angle(0)
        # self.right_motor.reset_angle(0)
        target_angle = motor_cycles * 360
        
        while self.left_motor.angle() < target_angle:
            # self.left_motor.run(speed)
            # self.right_motor.run(speed)
            self.drivebase.drive(speed, turn_rate)

            current_distance = self.distance_sensor.distance()
            self.hub.screen.print(turn_rate)
            if (current_distance > wall_distance + bias):
                # steer left
                self.hub.screen.print("left")
                # left_speed = speed - self.CORRECTION_SPEED
                # right_speed = speed + self.CORRECTION_SPEED
                turn_rate = turn_rate - self.CORRECTION_SPEED
            elif (current_distance < wall_distance - bias):
                # steer right
                self.hub.screen.print("right")
                # left_speed = speed + self.CORRECTION_SPEED
                # right_speed = speed - self.CORRECTION_SPEED
                turn_rate = turn_rate + self.CORRECTION_SPEED
            else:
                # steer clear
                self.hub.screen.print("straight")
                # left_speed = speed
                # right_speed = speed
                turn_rate = 0
            
            wait(10)

        self.left_motor.stop()
        self.right_motor.stop()

    def drive_until_line(self, speed=INITIAL_SPEED):
        "Drive forward until a white line is found"

        self.hub.screen.print("until line")
        self.hub.speaker.beep()

        self.drivebase.drive(speed, 0)
        while self.color_sensor.reflection() < self.WHITE:
            pass
        self.drivebase.stop()

    def drive_until_threshold_met(self, threshold_distance, speed, overshoot_time):
        "Drive forward until an object at threshold_distance is detected. Then keep driving for overshoot_time."
        "Positive threshold to detect objects entering the view, negative for objects leaving."
        if self.distance_sensor.distance() - threshold_distance < 0:
            return

        self.hub.screen.print("until threshold")
        self.hub.speaker.beep()

        self.drivebase.stop()
        self.right_motor.run(speed)
        self.left_motor.run(speed)

        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.distance_sensor.distance() - threshold_distance < 0:
                # keep driving for overshoot_time. wait is true to avoid a next loop iteration
                self.right_motor.run_time(speed, overshoot_time, then=Stop.BRAKE, wait=True)
                self.left_motor.run_time(speed, overshoot_time, then=Stop.BRAKE, wait=True)
                return


    def drive_until_box_found(self, threshold_distance, speed = INITIAL_SPEED, overshoot_time = 0):
        "Drive forward until an object nearer than threshold_distance is detected. Then keep driving for overshoot_time"
        self.drive_until_threshold_met(threshold_distance, speed, overshoot_time)
        

    def drive_until_box_lost(self, threshold_distance, speed = INITIAL_SPEED, overshoot_time = 0):
        "Drive forward until an object nearer than threshold_distance is not detected anymore. Then keep driving for overshoot_time"
        self.drive_until_threshold_met(-threshold_distance, speed, overshoot_time)