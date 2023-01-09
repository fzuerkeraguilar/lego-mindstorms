from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from controller.pcontroller import PController


class BridgeCrosser(Mode):

    RAMP_ANGLE = 15
    INITIAL_SPEED = 50
    WALL_DISTANCE = 572
    RAMP_LENGTH = 1050
    BRIDGE_LENGTH = 1050

    def __init__(self, color_sensor, distance_sensor, config, speed=INITIAL_SPEED):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.drivebase = config.get_drivebase(clean=True)

    def run(self):
        self.distance_sensor.set_down()
        self.drive_up_ramp()
        self.drivebase.turn(-90)
        self.drive_straight(1260)
        self.drivebase.turn(-90)
        self.drive_down_ramp()

    def drive_up_ramp(self):
        self.drivebase.reset()
        self.drivebase.drive(self.INITIAL_SPEED, 0)
        while self.drivebase.distance() < self.RAMP_LENGTH:
            if self.color_sensor.reflection() == 0:
                self.drivebase.stop()
                self.drivebase.straight(-40)
                return
            distance = self.distance_sensor.distance()
            self.hub.screen.print("Distance: ", distance)
            if distance > 150:
                self.drivebase.drive(self.INITIAL_SPEED, -15)    
            else :
                self.drivebase.drive(self.INITIAL_SPEED, 3)
        self.drivebase.stop()

    def drive_straight(self, drive_distance, speed=100):
        self.distance_sensor.set_angle(0)
        self.drivebase.reset()
        self.drivebase.drive(speed, 1)
        
        while self.drivebase.distance() < drive_distance:
            if self.color_sensor.reflection() == 0:
                self.drivebase.stop()
                self.drivebase.straight(-40)
                return
            distance = self.distance_sensor.distance()
            self.hub.screen.print("Distance: ", distance)
            if distance > 150:
                self.drivebase.drive(speed, -10)    
            else :
                self.drivebase.drive(speed, 1)
        self.drivebase.stop()

    def drive_down_ramp(self):
        self.drivebase.reset()
        self.drivebase.drive(self.INITIAL_SPEED, 0)
        while self.drivebase.distance() < self.RAMP_LENGTH:
            if self.color_sensor.color() == Color.BLUE:
                self.drivebase.stop()
                return
            if self.drivebase.distance() > 650:
                self.distance_sensor.set_up()
                self.drivebase.drive(self.INITIAL_SPEED, 0)
            else:
                distance = self.distance_sensor.distance()
                self.hub.screen.print("Distance: ", distance)
                if distance > 150:
                    self.drivebase.drive(self.INITIAL_SPEED, -10)    
                else:
                    self.drivebase.drive(self.INITIAL_SPEED, 1)
        self.drivebase.stop()

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
