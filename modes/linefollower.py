from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.tools import wait
from modes.mode import Mode

class LineFollower(Mode):
    BLACK = 6
    WHITE = 42
    THRESHOLD = (BLACK + WHITE) / 2
    GAIN = 3

    INITIAL_SPEED = 50
    TOP_SPEED = 80
    STEP_SIZE = 10
    WAIT_TIME = 5
    INITIAL_TURN = 50
    END_COLOR = Color.BLUE

    def __init__(self, ev3_hub, drivebase, right_motor, left_motor,
    color_sensor, distance_sensor, speed=INITIAL_SPEED):
        super().__init__(ev3_hub, drivebase, color_sensor, distance_sensor, speed)
        self.right_motor = right_motor
        self.left_motor = left_motor

    #TODO: Switch from reflection to rgb to detect the blue marker
    def follow_line(self):
        if self.distance_sensor.distance() < 100:
                self.avoid_obstacle()

        # Calculate the deviation from the threshold.
        reflection = self.color_sensor.reflection()
        deviation = reflection - self.THRESHOLD

        if reflection <= self.BLACK + 3:
            self.speed = self.INITIAL_SPEED
            if not self.find_line_direct():
                self.hub.speaker.beep(frequency=10000)
                self.drivebase.straight(150)

        self.speed = min(self.TOP_SPEED, self.speed + 1)
        if abs(deviation) > 7:
            self.speed = self.INITIAL_SPEED

        turn_rate = self.GAIN * deviation
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
        self.find_line_direct()
    
    def find_line_direct(self):

        self.hub.speaker.beep()
        self.drivebase.stop()
        self.hub.screen.print("Turn left")
        self.right_motor.run_time(500, 1300, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(-500, 1300, then=Stop.BRAKE, wait=False)
        wait(80)
        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.color_sensor.reflection() > self.THRESHOLD:
                self.hub.screen.print("Found line 1")
                self.right_motor.stop()
                self.left_motor.stop()
                return True
            pass 
        
        self.right_motor.run_time(-500, 2600, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(500, 2600, then=Stop.BRAKE, wait=False)
        wait(80)
        while (self.right_motor.speed() != 0 and self.left_motor.speed() != 0):
            if self.color_sensor.reflection() > self.THRESHOLD:
                self.hub.screen.print("Found line 2")
                self.right_motor.stop()
                self.left_motor.stop()
                return True
            pass
        wait(80)
        self.right_motor.run_time(500, 1300, then=Stop.BRAKE, wait=False)
        self.left_motor.run_time(-500, 1300, then=Stop.BRAKE, wait=True)
        return False

    def find_line_drivebase(self):
        self.drivebase.stop()
        self.hub.screen.print(self.drivebase.heading_control.pid())
        self.hub.screen.print(self.drivebase.heading_control.limits())
        degrees = 0

        while degrees < self.INITIAL_TURN:
            self.drivebase.turn(self.STEP_SIZE)
            degrees += self.STEP_SIZE
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(-self.INITIAL_TURN)
        degrees = 0
        while degrees > -90:
            self.drivebase.turn(-self.STEP_SIZE)
            degrees -= self.STEP_SIZE
            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(90)
        degrees = 0
        while degrees < 90:
            self.drivebase.turn(self.STEP_SIZE)
            degrees += self.STEP_SIZE

            if self.color_sensor.reflection() > self.THRESHOLD + 3:
                return True
        self.drivebase.turn(-90)
        return False

    def run(self):
        while Button.CENTER not in self.hub.buttons.pressed():
            self.follow_line()
        