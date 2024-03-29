from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Button
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from pybricks.tools import wait, StopWatch, DataLog
from controller.pcontroller import PController


class BoxPusher(Mode):
    WHITE = 30
    INITIAL_SPEED = 500
    SLOW_SPEED = 50
    MEDIUM_SPEED = 400
    THRESHOLD_DISTANCE = 300

    def __init__(
        self,
        color_sensor,
        distance_sensor,
        touch_sensor,
        config,
        speed=INITIAL_SPEED,
    ):
        super().__init__(color_sensor, distance_sensor, config, speed)
        self.touch_sensor = touch_sensor

    def run(self):
        self.drivebase.settings(self.speed, 2 * self.speed, self.speed // 2, self.speed)
        if self.find_start_pos() == False:
            return False
        if Button.CENTER in self.hub.buttons.pressed():
            return False
        if self.push_box() == False:
            return False
        if Button.CENTER in self.hub.buttons.pressed():
            return False
        if self.find_end_pos() == False:
            return False

    def find_start_pos(self):
        self.hub.screen.print("find start pos")
        self.hub.speaker.beep()

        self.drivebase.straight(200)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # align at left wall first tome to be able to drive straight
        self.drivebase.turn(-90)
        self.drivebase.straight(400)
        self.drivebase.straight(-230)
        self.drivebase.turn(90)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # drive forward until in reach of box
        self.drivebase.straight(1000)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # align at left wall
        self.drivebase.turn(-90)
        self.drivebase.straight(350)
        self.drivebase.straight(-70)
        self.drivebase.turn(90)

    def align_sensor(self):
        while self.distance_sensor.turn_motor.angle < 80:
            self.distance_sensor.turn_motor.run(200)

    def push_box(self):
        # find the box
        self.hub.screen.print("find box")
        self.distance_sensor.set_up()
        self.distance_sensor.set_angle(80)
        
        self.drive_until_box_found(self.THRESHOLD_DISTANCE)
        self.drivebase.reset()
        wait(50)
        self.drive_until_box_lost(self.THRESHOLD_DISTANCE)
        setback = self.drivebase.distance() // 2
        self.drivebase.straight(-setback)
        self.drivebase.turn(90)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # push box to the wall
        self.drivebase.straight(700)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # set back and turn
        self.drivebase.straight(-70)
        self.drivebase.turn(90)

        self.drivebase.straight(230)
        self.drivebase.turn(-90)
        self.drivebase.straight(250)
        self.drivebase.straight(-80)
        self.drivebase.turn(-90)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # push box to the wall
        self.drivebase.straight(550)
    
    def find_end_pos(self):
        # align at wall
        self.drivebase.straight(-70)
        self.drivebase.turn(90)
        self.drivebase.straight(200)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # face ramp
        self.drivebase.straight(-330)
        self.drivebase.turn(90)

        if Button.CENTER in self.hub.buttons.pressed():
            return False

        # find blue line
        self.drivebase.reset()
        self.distance_sensor.set_up()
        while self.drivebase.distance() < 550:
            self.drive_guided_straight(520)
        while self.color_sensor.color() != Color.BLUE:
            self.drivebase.drive(50, 0)
        self.drivebase.stop()   

    def drive_until_box_found(
        self, threshold_distance
    ):
        self.drivebase.drive(self.MEDIUM_SPEED, 0)

        times_found = 0
        while times_found < 5:
            dist = self.distance_sensor.distance()
            if dist < threshold_distance:
                times_found = times_found + 1
            else:
                times_found = 0

        self.drivebase.stop()

    def drive_guided_straight(self, wall_distance_mm):
        current_distance = self.distance_sensor.distance()
        if current_distance < wall_distance_mm:
            self.drivebase.drive(self.INITIAL_SPEED, -5)
        else:
            self.drivebase.drive(self.INITIAL_SPEED, 5)

    def drive_until_box_lost(
        self, threshold_distance
    ):
        self.drivebase.drive(self.SLOW_SPEED, 0)

        times_lost = 0
        while times_lost < 5:
            dist = self.distance_sensor.distance()
            if dist > threshold_distance:
                times_lost = times_lost + 1
            else:
                times_lost = 0

        self.drivebase.stop()
