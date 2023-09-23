import cv2 
import pyrealsense2 as rs
from ArdupilotControlApp.Master.PID_Kalman_Module import *
from ArdupilotControlApp.Master.UAVConcept import *

class PID_Tracker():
    def __init__(self, frequency, kalmanfilter: bool, antiwindup: bool):
        self.delta_t = 1 / frequency
        self.X_tracker_PID = PID(KP = 1, KI= 0, KD= 4, KN = 5, antiWindup= antiwindup)
        self.X_tracker_PID.setLims(-200,200)
        self.Y_tracker_PID = PID(KP = 0, KI= 0, KD= 0, KN = 5, antiWindup= antiwindup)
        self.Y_tracker_PID.setLims(-0,0)
        self.Z_tracker_PID = PID(KP = 500, KI= 0, KD= 0, KN = 5, antiWindup= antiwindup)
        self.Z_tracker_PID.setLims(-100,0)
        self.X_kalman_filter = Kalman()
        self.Y_kalman_filter = Kalman()
        self.Z_kalman_filter = Kalman()
        self.kalman_filter_on = kalmanfilter
        self.x_pwm, self.y_pwm, self.z_pwm = 1500, 1500, 1500
    
    def calculate_output_pwm(self, data, tracking_distance):
        try:
            if data != None:
                x, y, z = data
                if (self.kalman_filter_on):
                    x_kalman = self.X_kalman_filter.Filter(x)[0]
                    y_kalman = self.Y_kalman_filter.Filter(y)[0]
                    z_kalman = self.Z_kalman_filter.Filter(z)[0]
                else: 
                    x_kalman = x
                    y_kalman = y
                    z_kalman = z
                    
                self.x_pwm = 1500 + self.X_tracker_PID.compute(float(x_kalman), 0, self.delta_t)
                self.y_pwm = 1500 + self.Y_tracker_PID.compute(float(y_kalman), 0, self.delta_t)
                self.z_pwm = 1500 - self.Z_tracker_PID.compute(float(z_kalman), tracking_distance, self.delta_t)
                
                #print(int(self.x_pwm), int(self.y_pwm), int(self.z_pwm))
                
                #Forward and Backward
                
                # if self.z_pwm < 1600 and self.z_pwm > 1400:
                #     if self.x_pwm < 1800 and self.x_pwm > 1200:
                #         #Stay
                #         return [1501, 1501, 1501]
                #     elif self.x_pwm >= 1800 or self.x_pwm <= 1200:
                #         #Turn to track object
                #         if self.z_pwm > 1500:
                #             return [int(self.x_pwm), int(self.y_pwm), self.z_pwm]
                #         elif self.z_pwm < 1500:
                #             return [3000-int(self.x_pwm), int(self.y_pwm), int(self.z_pwm)]
                
                if self.z_pwm > 1580:
                    #Go foward
                    return [int(self.x_pwm), int(self.y_pwm), int(self.z_pwm)]
                
                if self.z_pwm <= 1580 and self.z_pwm >= 1470:
                    #Stay
                    return [1500, 1500, 1500]
                
                elif self.z_pwm < 1470:
                    #Go backward
                    return [3000-int(self.x_pwm), int(self.y_pwm), int(self.z_pwm)]
            
            else:
                return [1500,1500,1500]
        
        except:
            pass
    
class Tracker():
    def __init__(self, tracker_type):
        """
        Args:
            type (_str_):   "KCF" fast tracking
            
                                "MIL" slow but good tracking
                          
                                "CSRT" good tracking
        """
        self.pipeline = rs. pipeline()  # type: ignore
        self.config = rs.config() # type: ignore
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) # type: ignore
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # type: ignore
        self.profile = self.pipeline.start(self.config)

        if tracker_type == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()
        elif tracker_type == "MIL":
            self.tracker = cv2.TrackerMIL_create()
        elif tracker_type == "KCF":
            self.tracker = cv2.TrackerKCF_create()
        else:
            raise ValueError("Unknown tracker type")
        
        for i in range(30):
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
        self.roi = cv2.selectROI("Select ROI",color_image, False, False) # type: ignore
        cv2.destroyAllWindows()
        self.tracker.init(color_image, self.roi) # type: ignore
        
    def tracking_object(self):
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            align = rs.align(rs.stream.color) # type: ignore
            frameset = align.process(frames)
            align_depth_frame = frameset.get_depth_frame()
            ret, bbox = self.tracker.update(color_image)
            if ret:
                # draw the bounding box on the frame
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                cv2.rectangle(color_image, (x, y, w, h), (0, 255, 0), 2)
                x_center = x + w/2
                y_center = y + h/2
                distance = np.asanyarray(align_depth_frame.get_distance(int(x_center),int(y_center)))
                data = [float(x_center-320), float(y_center-240), float(distance)]
            else:
                # display a failure message
                cv2.putText(color_image, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                data = None
                
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                self.pipeline.stop()
                exit(0)
                
            cv2.imshow("Tracker", color_image)
            return data
            
        except Exception as e:
            print(e)