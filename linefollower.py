from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Stop
from pybricks.robotics import DriveBase
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.tools import wait


class LineFollower:
    BLACK = 6
    WHITE = 42
    THRESHOLD = (BLACK + WHITE) / 2
    GAIN = 3

    INITIAL_SPEED = 50
    TOP_SPEED = 80
    STEP_SIZE = 14
    WAIT_TIME = 5
    INITIAL_TURN = 50
    END_COLOR = Color.BLUE

    def __init__(self, drivebase, right_motor, left_motor, color_sensor, touch_sensor, distance_sensor, hub, speed=self.INITIAL_SPEED):
        self.drivebase = drivebase
        self.right_motor = right_motor
        self.left_motor = left_motor
        self.color_sensor = color_sensor
        self.touch_sensor = touch_sensor
        self.distance_sensor = distance_sensor
        self.speed = speed
        self.hub = hub


    def follow_line(self):
        while True:

            if self.distance_sensor.distance() < 100:
                self.avoid_obstacle()

            # Calculate the deviation from the threshold.
            reflection = self.color_sensor.reflection()
            deviation = reflection - self.THRESHOLD

            if reflection <= self.BLACK + 3:
                self.speed = self.INITIAL_SPEED
                if not self.find_line():
                    self.hub.speaker.beep(duration=1000)
                    self.drivebase.straight(150)

            self.speed = min(self.TOP_SPEED, self.speed + 1)
            if abs(deviation) > 7:
                self.speed = self.INITIAL_SPEED

            turn_rate = self.GAIN * deviation
            self.hub.screen.print(deviation)
            self.drivebase.drive(self.speed, turn_rate)
    
    def avoid_obstacle(self):
        self.drivebase.stop()
        self.drivebase.turn(90)
        self.drivebase.straight(200)
        self.drivebase.turn(-90)
        self.drivebase.straight(300)
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.turn(90)
        self.find_line()
    
    def find_line(self):
        # degrees = 0

        # self.hub.speaker.beep()
        # while degrees < self.INITIAL_TURN:
        #     self.drivebase.turn(self.STEP_SIZE)
        #     degrees += self.STEP_SIZE
        #     if self.color_sensor.reflection() > self.THRESHOLD + 3:
        #         return True
        # self.drivebase.turn(-self.INITIAL_TURN)
        # degrees = 0
        # while degrees > -90:
        #     self.drivebase.turn(-self.STEP_SIZE)
        #     if self.color_sensor.reflection() > self.THRESHOLD + 3:
        #         return True
        # self.drivebase.turn(90)
        # degrees = 0
        # while degrees < 90:
        #     self.drivebase.turn(self.STEP_SIZE)
        #     degrees += self.STEP_SIZE

        #     if self.color_sensor.reflection() > self.THRESHOLD + 3:
        #         return True
        # self.drivebase.turn(-90)
        # return False
        self.hub.speaker.beep()
        self.drivebase.stop()
        self.right_motor.run_time(500, 1300, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(-500, 1300, then=Stop.BRAKE, wait=False)
        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                self.right_motor.stop()
                self.left_motor.stop()
                return True
            pass 
        self.right_motor.stop()
        self.left_motor.stop()

        self.right_motor.run_time(-500, 1300, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(500, 1300, then=Stop.BRAKE, wait=False)
        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                self.right_motor.stop()
                self.left_motor.stop()
                return True
            pass
        self.right_motor.stop()
        self.left_motor.stop() 
        return False


            


    
    def run(self):
        self.follow_line()
        