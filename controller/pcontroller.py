class PController:
    def __init__(target, Kp):
        self.target = target
        self.Kp = Kp

    def correction(self, current):
        deviation = self.target - current
        return self.Kp * deviation
    
