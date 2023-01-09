from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import TouchSensor, ColorSensor
from modes.mode import Mode
from pybricks.tools import wait
from controller.pcontroller import PController


class BoxPusher(Mode):
    WHITE = 30
    INITIAL_SPEED = 300
    SLOW_SPEED = 50
    CORRECTION_SPEED = 2
    DISTANCE_BIAS = 5
    THRESHOLD_DISTANCE = 300

    UP = 65
    DOWN = 0

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
        self.drivebase.settings(self.speed, None, self.speed)
        self.find_start_pos()
        self.push_box()
        self.find_end_pos()

    def find_start_pos(self):
        self.hub.screen.print("find start pos")
        self.hub.speaker.beep()

        self.drivebase.straight(100)

        # align at left wall first tome to be able to drive straight
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.straight(-200)
        self.drivebase.turn(90)

        # drive forward until in reach of box
        self.drivebase.straight(1100)

        # align at left wall
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.straight(-70)
        self.drivebase.turn(90)

    def align_sensor(self):
        while self.distance_sensor.turn_motor.angle < 80:
            self.distance_sensor.turn_motor.run(200)

    def push_box(self):
        self.hub.speaker.beep()
        # find the box
        self.hub.screen.print("find box")
        self.distance_sensor.set_up()
        self.distance_sensor.set_angle(80)
        # self.distance_sensor.set_up()
        # self.distance_sensor.set_angle(80)
        # self.align_sensor()
        self.drive_until_box_found(self.THRESHOLD_DISTANCE)
        self.drive_until_box_lost(self.THRESHOLD_DISTANCE)
        self.drivebase.straight(-100)
        self.drivebase.turn(90)

        # push box to the wall
        self.hub.screen.print("push box 1")
        self.drivebase.straight(700)

        # set back and turn
        self.drivebase.straight(-70)
        self.drivebase.turn(90)

        self.drivebase.straight(230)
        self.drivebase.turn(-90)
        self.drivebase.straight(200)
        self.drivebase.straight(-60)
        self.drivebase.turn(-90)

        # push box to the wall
        self.drivebase.straight(550)
    
    def find_end_pos(self):
        self.hub.screen.print("find end pos")
        self.hub.speaker.beep()

        self.drivebase.straight(-70)
        self.drivebase.turn(90)
        self.drivebase.straight(200)
        self.drivebase.straight(-330)
        self.drivebase.turn(90)
        # align at back wall
        # self.drivebase.straight(-230)

        # # set back
        # self.drivebase.straight(-50)
        # self.drivebase.turn(90)
        
        # self.drivebase.straight(300)
        # self.drivebase.stop()
        # self.drivebase.turn(-90)

        # find blue line
        self.drivebase.straight(550)
        while self.color_sensor.color() != Color.BLUE:
            self.drivebase.drive(50, 0)
        self.drivebase.stop()   

    def drive_guided_straight(
        self, distance, wall_distance, speed=INITIAL_SPEED, bias=DISTANCE_BIAS
    ):
        "Drive straight for motor_cycles with guidance from the distance sensor"
        self.hub.screen.print("guided straight")
        self.hub.speaker.beep()

        wall_distance = wall_distance
        controller = PController(wall_distance, 0.1)

        # use drivebase to detect driven length

        self.drivebase.reset()
        while self.drivebase.distance() < distance:
            # correct angle to drive straight
            current_distance = self.distance_sensor.distance()
            turn_rate = min(controller.correction(current_distance), 3)
            self.drivebase.drive(speed, turn_rate)
            self.hub.screen.print(turn_rate)
            
            if self.color_sensor.color() == Color.BLUE:
                self.hub.speaker.beep()
                break

        self.drivebase.stop()

    def drive_until_line(self, speed=INITIAL_SPEED):
        "Drive forward until a white line is found"

        self.hub.screen.print("until line")
        self.hub.speaker.beep()

        self.drivebase.drive(speed, 0)
        while self.color_sensor.reflection() < self.WHITE:
            continue
        self.drivebase.stop()

    # def drive_until_threshold_met(self, threshold_distance, speed, overshoot_time):

    def drive_until_box_found(
        self, threshold_distance, speed=INITIAL_SPEED, overshoot_time=0
    ):
        "Drive forward until an object at threshold_distance is detected. Then keep driving for overshoot_time."
        "Positive threshold to detect objects entering the view, negative for objects leaving."
        self.hub.screen.print("until threshold")
        self.hub.speaker.beep()

        self.drivebase.drive(speed, 0)

        while self.distance_sensor.distance() > threshold_distance:
            self.hub.screen.print(self.distance_sensor.distance())
            pass

        # wait(overshoot_time) # keep driving for overshoot_time.
        # self.drivebase.straight(50)
        self.drivebase.stop()


    def drive_until_box_lost(
        self, threshold_distance, speed=INITIAL_SPEED, overshoot_time=0
    ):
        # "Drive forward until an object at threshold_distance is detected. Then keep driving for overshoot_time."
        # "Positive threshold to detect objects entering the view, negative for objects leaving."
        self.hub.screen.print("until threshold")
        self.hub.speaker.beep()

        self.drivebase.drive(self.SLOW_SPEED, 0)

        while self.distance_sensor.distance() < threshold_distance:
            self.hub.screen.print(self.distance_sensor.distance())
            pass

        # wait(overshoot_time) # keep driving for overshoot_time.
        self.hub.speaker.beep(frequency=8000)
        self.drivebase.stop()
