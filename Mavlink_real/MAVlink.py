from pymavlink import mavutil
import time
from enum import Enum

class ProgressStatus(Enum):
    OK = 0
    ERROR = 1

class MyMAVlink():
    def __init__(self, connection_string, baudrate):
        self.connection = mavutil.mavlink_connection(connection_string, baud = baudrate)
        self.boot_time = time.time()
        self.connection_status = self.wait_for_connection(10)
        if self.connection_status == ProgressStatus.OK:
            self.target_system = self.connection.target_system
            self.target_component = self.connection.target_component
        elif self.connection_status == ProgressStatus.ERROR:
            self.error_flag = True
            raise ValueError("Invalid MAVlink connection")
        
    def wait_for_connection(self, wait_timeout) -> ProgressStatus:
        """
        Sends a ping to stabilish the UDP communication and awaits for a response
        """
        msg = None
        wait_time = 0
        while not msg:
            self.connection.mav.ping_send(
                int(time.time() * 1e6), # Unix time in microseconds
                0,# Ping number
                0,# Request ping of all systems
                0 # Request ping of all components
                )
            msg = self.connection.recv_match()
            wait_time += 1
            if wait_time == wait_timeout:
                break
            time.sleep(1)
    
        if msg != None:
            return ProgressStatus.OK
        else: 
            return ProgressStatus.ERROR
        
    def arm_disarm(self, data):
        #data = 0 DISARM
        #data = 1 ARM
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            data, 0, 0, 0, 0, 0, 0
        )
    
    def take_off(self, data):
        altitude = data
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,0,0,0,0,0,altitude
        )
    
    def arm_and_takeoff(self, height):
        self.arm_disarm(1)
        time.sleep(2)
        self.take_off(height)
    
    def return_to_land(self):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
            0,
            0,0,0,0,0,0,0
        )
    
    def land(self):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_MAV_LAND,
            0, 0, 0, 0, 0, 0, 0
        )
    
    def set_mode(self, mode):
        """_summary_

        Args:
            mode (_int_):   3 == auto
            
                            4 == guided
                            
                            5 == loiter
                            
                            6 == RTL
                            
                            9 == land
        """
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,
            0,
            1, mode,
            0, 0, 0, 0, 0
        )
        
    def set_home(self, data):
        mav_frame = 10
        latitude, longitude, altitude = data
        self.connection.mav.command_int_send(
            self.target_system,
            self.target_component,
            mav_frame,
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,
            0,
            0,
            0, 
            0, 
            0, 
            0,
            latitude,
            longitude,
            altitude
        )
    
    def set_frame_position(self, data):
        #Copter:
            #Use Position : 0b110111111000 / 0x0DF8 / 3576 (decimal)

        type_mask = 3576
        x, y, z = data
        
        self.connection.mav.set_position_target_local_ned_send(
            int(1e3 * (time.time() - self.boot_time)),          #time_boot_ms
            self.target_system,
            self.target_component,       #target_system, taget_component
            8, #frame valid options are: MAV_FRAME_LOCAL_NED = 1, MAV_FRAME_LOCAL_OFFSET_NED = 7, MAV_FRAME_BODY_NED = 8, MAV_FRAME_BODY_OFFSET_NED = 9
            type_mask,       #type_mask (only position)
            x, y, z,    #x, y, z positions in m
            0, 0, 0,    #vy, vy, vz velocity in m/s
            0, 0, 0,    #ax, ay, az acceleration
            0, 0        #yaw, yaw_rate
        )
    
    def do_reposition(self, data):
        mavframe = 10
        latitude, longitude, altitude = data
        
        self.connection.mav.command_int_send(
            self.target_system,
            self.target_component,
            mavframe,
            mavutil.mavlink.MAV_CMD_DO_REPOSITION,
            0, 0,
            -1, 1,
            0, 0,
            latitude, longitude, altitude
        )
        
    def set_speed(self, data):
        """_summary_

        Args:
            data (_type_): [speedtype:(0=Airspeed, 1=Ground Speed, 2=Climb Speed, 3=Descent Speed), speed (m/s)]
        """
        speedtype, speed = data
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
            0,
            speedtype,
            speed,
            -1,0,0,0,0
        )
    
    def mission_interaction(self, data):
        """_summary_

        Args:
            data (_int_): : 0: Pause current mission or reposition command, hold current position. 1: Continue mission. 
        """
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_DO_PAUSE_CONTINUE,
            0,
            data,
            0, 0, 0, 0, 0, 0
        )

    def set_current_mission(self, mission_id):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MISSION_CURRENT,
            0,
            mission_id,
            1, #reset mission true = 1, false = 0
            0, 0, 0, 0, 0
        )
        
    def rc_channel_override(self, data):
        channels, pwms = data
        rc_channel_value = [65535 for _ in range(8)]
        for i in range(len(channels)):
                rc_channel_value[channels[i] - 1] = pwms[i]
        self.connection.mav.rc_channels_override_send(
            self.target_system,
            self.target_component,
            *rc_channel_value
        )
        
    def get_gps_position(self):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,
            33,
            0, 0, 0, 0, 0, 0
        )
        time.sleep(0.5)
        time_out = 10
        timer = 0
        while True:
            msg = self.connection.recv_match(type = "GLOBAL_POSITION_INT", blocking = False)
            timer += 1
            if timer >= time_out:
                print("Time out. No GPS recieved")
                break
            if not msg:
                continue
            else:
                print(msg)
                # print(f"Got message: {msg.get_type()}")
                # print(f"Latitude, Longitude, : {msg.lat/1e7, msg.lon/1e7}")
                # print(f"Altitude ASL, Altitude AGL: {msg.alt/1e3, msg.relative_alt/1e3}")
                break
            
            
    def move_forward(self, distance):
        self.set_frame_position([distance, 0, 0])
    
    def move_backward(self, distance):
        self.set_frame_position([-distance, 0, 0])
    
    def move_left(self, distance):
        self.set_frame_position([0, -distance, 0])
        
    def move_right(self, distance):
        self.set_frame_position([0, distance, 0])
        
    def move_up(self, distance):
        self.set_frame_position([0, 0, -distance])
        
    def move_down(self, distance):
        self.set_frame_position([0, 0, distance])