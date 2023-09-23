import numpy as np

class PID():
    def __init__(self, KP, KI, KD, KN, antiWindup=False):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.kn = KN #Filter coefficient 
        self.error_last = 0
        self.integral_error = 0 
        self.saturation_max = None
        self.saturation_min = None
        self.antiWindup = antiWindup
    def compute(self, pos, target, dt):
        error = target - pos
        derivative_error = ((error - self.error_last)* self.kn) / (1+ self.kn * dt)
        output = self.kp*error + self.ki*self.integral_error + self.kd*derivative_error
        self.error_last = error
        
        if(abs(output)>= self.saturation_max and (((error>=0) and (self.integral_error>=0))or((error<0) and (self.integral_error<0)))):
            if (self.antiWindup):
                #no integration
                self.integral_error = self.integral_error
            else:
                #if no antiWindup rectangular integration     
                self.integral_error += error * dt
        else:
            self.integral_error += error * dt
        
        if output > self.saturation_max and self.saturation_max is not None:
            output = self.saturation_max
        elif output < self.saturation_min and self.saturation_min is not None:
            output = self.saturation_min
        return output
    def setLims(self, min, max):
        self.saturation_max = max
        self.saturation_min = min
        
class Kalman:
    def __init__(self):
        dt = 0.01
        self.x = np.array([[0],[0]])        #Initial state
        self.P = np.array([[5,0],[0,5]])    #Initial state covariance
        self.A = np.array([[1,dt],[0,1]])   #Transition matrix
        self.H = np.array([[1,0]])          #Observation matrix
        self.HT = np.array([[1],[0]])      
        self.R = 5                       #Covariance of observation noise
        self.Q = np.array([[1,0],[0,3]])    #Covariance of process noise
    def Filter(self, z):
        #Predict State Forward
        x_p = self.A.dot(self.x)
        #Predict Covariance Forward
        P_p = self.A.dot(self.P).dot(self.A.T) + self.Q 
        #Compute Kalman Gain
        S = self.H.dot(P_p).dot(self.HT) + self.R 
        K = P_p.dot(self.HT)*(1/S)

        #Estimate State
        residual = z - self.H.dot(x_p)
        self.x = x_p + K*residual

        #Estimate Covariance
        self.P = P_p - K.dot(self.H).dot(P_p)
        
        return [self.x[0], self.x[1], self.P]