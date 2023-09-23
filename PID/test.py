from myPID import myPID
import time

KP = 30
KD = 300
KI = 2
targetHeight = 30  # m
initialHeight = 0  # m
droneWeight = 10  # kg
gravity = 9.81  # kg/m2
testObject = myPID(KP=KP, KI=KI, KD=KD, targetValue=targetHeight)
testObject.updateInitialValue(initialHeight)
testObject.enableAntiWindup(state=True, maxIntergratedValue=110, minIntergratedValue=0)
testObject.enableLimitOutput(state=True, maxOutputValue=1000, minOutputValue=0)
timeTotal = 0
dt = 0.1

while True:
    thrust = testObject.calculateOutputValue()

    net_force = thrust - droneWeight * gravity
    acceleration = net_force / droneWeight
    initialHeight += 0.5 * acceleration * dt**2

    P, I, D = testObject.getPIDValue()
    print(
        f"Time: {timeTotal:.1f}s | Height: {initialHeight:.2f}m | Thrust: {thrust:.2f}N | P:{P:.2f} | I: {I:.2f} | D:{D:.2f}"
    )

    timeTotal += dt
    testObject.updateInitialValue(initialHeight)
    time.sleep(dt)
