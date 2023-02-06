from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from controller.pcontroller import PController


class BridgeCrosser(Mode):

    RAMP_ANGLE = 15
    INITIAL_SPEED = 70
    UP_SPEED = 200
    STRAIGHT_SPEED = 200
    DOWN_SPEED = 100
    WALL_DISTANCE = 572
    RAMP_LENGTH = 1050
    BRIDGE_LENGTH = 1050

    def __init__(self, color_sensor, distance_sensor, touch_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sensor
        self.drivebase = config.get_drivebase(clean=True)

    def run(self):
        self.distance_sensor.set_down()
        if self.drive_up_ramp() == False:
            return False
        self.drivebase.turn(-90)
        if self.drive_straight(1260) == False:
            return False
        self.drivebase.turn(-90)
        if self.drive_down_ramp() == False:
            return False

    def drive_up_ramp(self):
        self.drivebase.reset()
        while self.drivebase.distance() < self.RAMP_LENGTH + 30: 
            if Button.CENTER in self.hub.buttons.pressed():
                self.drivebase.stop()
                return False
            distance = self.distance_sensor.distance()
            if distance > 150:
                self.drivebase.drive(self.UP_SPEED, -15)    
            else:
                self.drivebase.drive(self.UP_SPEED, 3)
        self.drivebase.stop()

    def drive_straight(self, drive_distance):
        self.distance_sensor.set_angle(0)
        self.drivebase.reset()
        while self.drivebase.distance() < drive_distance:
            if Button.CENTER in self.hub.buttons.pressed():
                self.drivebase.stop()
                return False
            if self.color_sensor.reflection() == 0:
                self.drivebase.stop()
                self.drivebase.straight(-40)
                return
            distance = self.distance_sensor.distance()
            if distance > 150:
                self.drivebase.drive(self.STRAIGHT_SPEED, -10)    
            else:
                self.drivebase.drive(self.STRAIGHT_SPEED, 3)
        self.drivebase.stop()

    def drive_down_ramp(self):
        self.drivebase.reset()
        while self.drivebase.distance() < self.RAMP_LENGTH - 200:
            if Button.CENTER in self.hub.buttons.pressed():
                self.drivebase.stop()
                return False
            if self.color_sensor.color() == Color.BLUE:
                self.drivebase.stop()
                return
            if self.drivebase.distance() > 620:
                self.try_to_enter_hole()
                return
            else:
                distance = self.distance_sensor.distance()
                if distance > 150:
                    self.drivebase.drive(self.DOWN_SPEED, -10)    
                else:
                    self.drivebase.drive(self.DOWN_SPEED, 1)
        self.drivebase.stop()

    def try_to_enter_hole(self):
        self.distance_sensor.set_up()
        self.drivebase.drive(self.DOWN_SPEED, 0)
        while True:
            if self.color_sensor.color() == Color.BLUE:
                self.drivebase.stop()
                return True
            if self.touch_sensor.pressed_right():
                self.drivebase.straight(-100)
                self.drivebase.turn(-10)
            if self.touch_sensor.pressed_left():
                self.drivebase.straight(-100)
                self.drivebase.turn(10)
            self.drivebase.drive(self.DOWN_SPEED, 0)

    def play_music(self):
        frequency = [
            659.25511, 493.8833, 523.25113, 587.32954, 523.25113, 493.8833, 440.0, 440.0, 
            523.25113, 659.25511, 587.32954, 523.25113, 493.8833, 523.25113, 587.32954, 
            659.25511, 523.25113, 440.0, 440.0, 440.0, 493.8833, 523.25113, 587.32954, 
            698.45646, 880.0, 783.99087, 698.45646, 659.25511, 523.25113, 659.25511, 
            587.32954, 523.25113, 493.8833, 493.8833, 523.25113, 587.32954, 659.25511, 
            523.25113, 440.0, 440.0
        ]
        duration = [
            406.250, 203.125, 203.125, 406.250, 203.125, 203.125, 406.250, 203.125, 
            203.125, 406.250, 203.125, 203.125, 609.375, 203.125, 406.250, 406.250, 
            406.250, 406.250, 203.125, 203.125, 203.125, 203.125, 609.375, 203.125, 
            406.250, 203.125, 203.125, 609.375, 203.125, 406.250, 203.125, 203.125, 
            406.250, 203.125, 203.125, 406.250, 406.250, 406.250, 406.250, 406.250
        ]

        for i in range(0, len(frequency)):
            self.hub.screen.print("Beep", frequency[i])
            self.hub.speaker.beep(frequency[i], duration[i])
            yield
        
        while True:
            yield
