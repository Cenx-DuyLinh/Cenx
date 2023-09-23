class myPID:
    def __init__(self, KP: float, KI: float, KD: float, targetValue: float) -> None:
        self.KP = KP
        self.KI = KI
        self.KD = KD
        self.targetValue = targetValue
        self.initialValue = 0
        self.antiWindupState = False
        self.limitOutputState = False
        self.maxIntergratedValue = 0
        self.minIntergratedValue = 0
        self.maxOutputValue = 0
        self.minOutputValue = 0
        self.prevError = 0
        self.integrator = 0

    def updateInitialValue(self, value) -> None:
        self.initialValue = value

    def enableAntiWindup(
        self, state: bool, maxIntergratedValue: float, minIntergratedValue: float
    ) -> None:
        self.antiWindupState = state
        self.maxIntergratedValue = maxIntergratedValue
        self.minIntergratedValue = minIntergratedValue

    def enableLimitOutput(
        self,
        state: bool,
        maxOutputValue: float,
        minOutputValue: float,
    ) -> None:
        self.limitOutputState = state
        self.maxOutputValue = maxOutputValue
        self.minOutputValue = minOutputValue

    def calculateOutputValue(self) -> float:
        error = self.targetValue - self.initialValue

        self.integrator += self.KI * error

        if self.antiWindupState is True:
            if self.integrator > self.maxIntergratedValue:
                self.integrator = self.maxIntergratedValue
            elif self.integrator < self.minIntergratedValue:
                self.integrator = self.minIntergratedValue

        self.P = self.KP * error
        self.I = self.integrator
        self.D = self.KD * (error - self.prevError)
        self.prevError = error

        output = self.P + self.I + self.D
        if self.limitOutputState is True:
            if output >= self.maxOutputValue:
                output = self.maxOutputValue
            elif output <= self.minOutputValue:
                output = self.minOutputValue
        return output

    def getPIDValue(self):
        return self.P, self.I, self.D
