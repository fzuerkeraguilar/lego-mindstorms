from pybricks.tools import wait
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.ev3devices import ColorSensor
from pybricks.robotics import DriveBase
import json


class Calibration:
    def __init__(self, l_motor, r_motor, color_sensor):
        self.hub = EV3Brick()
        self.left_motor = l_motor
        self.right_motor = r_motor
        self.color_sensor = color_sensor
        self.config = json.load(open("config.json"))

    def get_black():
        return self.config["black_reflection"]

    def get_white():
        return self.config["white_reflection"]

    def get_wb(self):
        return self.config["white_reflection"], self.config["black_reflection"]

    def get_drivebase(self, clean=False):
        if clean:
            return DriveBase(
                self.left_motor,
                self.right_motor,
                self.config["clean_drivebase"]["wheel_diameter"],
                self.config["clean_drivebase"]["wheel_base"],
            )
        else:
            return DriveBase(
                self.left_motor,
                self.right_motor,
                self.config["dusty_drivebase"]["wheel_diameter"],
                self.config["dusty_drivebase"]["wheel_base"],
            )

    def get_wheel_diameter(self, clean=False):
        if clean:
            return self.config["clean_drivebase"]["wheel_diameter"]
        else:
            return self.config["dusty_drivebase"]["wheel_diameter"]

    def get_wheel_base(self, clean=False):
        if clean:
            return self.config["clean_drivebase"]["wheel_base"]
        else:
            return self.config["dusty_drivebase"]["wheel_base"]

    def caibrate_color_sensor(self):
        original_black = self.config["black_reflection"]
        original_white = self.config["white_reflection"]
        black_reflection = 0
        white_reflection = 0
        while True:
            self.hub.screen.clear()
            white_reflection = self.color_sensor.reflection()
            self.hub.screen.draw_text(0, 0, "White: " + str(white_reflection))
            wait(150)
            buttons = self.hub.buttons.pressed()
            if Button.CENTER in buttons:
                break
            if Button.LEFT in buttons:
                return original_black, original_white
        wait(200)
        while True:
            self.hub.screen.clear()
            black_reflection = self.color_sensor.reflection()
            self.hub.screen.draw_text(0, 0, "Black: " + str(black_reflection))
            wait(150)
            buttons = self.hub.buttons.pressed()
            if Button.CENTER in buttons:
                break
            if Button.LEFT in buttons:
                self.hub.screen.clear()
                return original_black, original_white
        self.hub.screen.clear()
        return (black_reflection, white_reflection)

    def calibrate_drivebase(self, clean=False):
        wheel_base, wheel_diameter = 0, 0
        self.drivebase = self.get_drivebase(clean)
        if clean:
            wheel_base = self.config["clean_drivebase"]["wheel_base"]
            wheel_diameter = self.config["clean_drivebase"]["wheel_diameter"]
        else:
            wheel_base = self.config["dusty_drivebase"]["wheel_base"]
            wheel_diameter = self.config["dusty_drivebase"]["wheel_diameter"]
        delta_wheel_base = 0
        delta_wheel_diameter = 0
        while True:
            self.hub.screen.clear()
            self.hub.screen.print(
                "Wheel base: " + str(wheel_base + delta_wheel_base) + "mm"
            )
            self.hub.screen.print("Original: " + str(wheel_base) + "mm")
            wait(150)
            buttons = self.hub.buttons.pressed()
            if Button.CENTER in buttons:
                self.drivebase = DriveBase(
                    self.left_motor,
                    self.right_motor,
                    wheel_diameter + delta_wheel_diameter,
                    wheel_base + delta_wheel_base,
                )
                self.drivebase.turn(360)
            if Button.UP in buttons:
                delta_wheel_base += 1
            if Button.DOWN in buttons:
                delta_wheel_base -= 1
            if Button.RIGHT in buttons:
                break
            if Button.LEFT in buttons:
                return wheel_base, wheel_diameter
        while True:
            self.hub.screen.clear()
            self.hub.screen.print(
                "Wheel dia.: "
                + str(wheel_diameter + delta_wheel_diameter)
                + "mm"
            )
            self.hub.screen.print("Original: " + str(wheel_diameter) + "mm")
            wait(150)
            buttons = self.hub.buttons.pressed()
            if Button.CENTER in buttons:
                self.drivebase = DriveBase(
                    self.left_motor,
                    self.right_motor,
                    wheel_diameter + delta_wheel_diameter,
                    wheel_base + delta_wheel_base,
                )
                self.drivebase.straight(1000)
            if Button.UP in buttons:
                delta_wheel_diameter += 1
            if Button.DOWN in buttons:
                delta_wheel_diameter -= 1
            if Button.RIGHT in buttons:
                break
            if Button.LEFT in buttons:
                return wheel_base, wheel_diameter
        self.drivebase.stop()
        return wheel_base + delta_wheel_base, wheel_diameter + delta_wheel_diameter

    def run(self):
        options = [
            "Dusty Drivebase",
            "Clean Drivebase",
            "Color Sensor",
            "Save to file",
            "Exit",
        ]
        option = 0
        while True:
            self.hub.screen.clear()
            self.hub.screen.print("Select a calibration to run:")
            self.hub.screen.print(options[option])
            wait(150)
            buttons = self.hub.buttons.pressed()
            if Button.UP in buttons:
                option = (option - 1) % len(options)
            if Button.DOWN in buttons:
                option = (option + 1) % len(options)
            if Button.CENTER in buttons:
                if option == 0:
                    wheel_base, wheel_diameter = self.calibrate_drivebase()
                    self.config["dusty_drivebase"]["wheel_base"] = wheel_base
                    self.config["dusty_drivebase"]["wheel_diameter"] = wheel_diameter
                elif option == 1:
                    wheel_base, wheel_diameter = self.calibrate_drivebase(clean=True)
                    self.config["clean_drivebase"]["wheel_base"] = wheel_base
                    self.config["clean_drivebase"]["wheel_diameter"] = wheel_diameter
                elif option == 2:
                    black_reflection, white_reflection = self.caibrate_color_sensor()
                    self.config["black_reflection"] = black_reflection
                    self.config["white_reflection"] = white_reflection
                elif option == 3:
                    with open("config.json", "w") as f:
                        json.dump(self.config, f)
                elif option == 4:
                    break
