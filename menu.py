from pybricks.parameters import Button
from pybricks.tools import wait


class Menu:
    def __init__(self, hub, modes):
        # @param hub: ev3hub
        # @param modes: [(name: String, value: any, next: any?)]
        self.hub = hub
        self.modes = modes

    def show(self, autoselect=None):
        if autoselect != None:
            return self.modes[autoselect][1], self.modes[autoselect][2]

        active_mode = 0

        while True: 
            self.hub.screen.clear()
            self.hub.screen.print("Select:")
            self.hub.screen.print(self.modes[active_mode][0])

            wait(150)

            buttons = self.hub.buttons.pressed()
            if Button.UP in buttons:
                active_mode = (active_mode - 1) % len(self.modes)

            elif Button.DOWN in buttons:
                active_mode = (active_mode + 1) % len(self.modes)

            elif Button.LEFT in buttons:
                return None, None

            elif Button.RIGHT in buttons or Button.CENTER in buttons:
                return self.modes[active_mode][1], self.modes[active_mode][2]
