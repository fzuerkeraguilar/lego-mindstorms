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
        self.drivebase.turn(-90)
        self.drive_straight()
        self.drivebase.turn(-90)
        self.drive_down()

    def drive_up(self):
        self.drivebase.straight(1050)

    def drive_straight(self):
        target_distance = 1260
        speed = 100

        self.drivebase.reset()
        self.drivebase.drive(speed, 0)

        music = self.play_music()
        
        while self.drivebase.distance() < target_distance:
            next(music)

        self.drivebase.stop()

    def drive_down(self):
        self.drivebase.straight(1000)

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
            # self.hub.speaker.beep(frequency[i], duration[i])
            yield
        
        while True:
            yield
