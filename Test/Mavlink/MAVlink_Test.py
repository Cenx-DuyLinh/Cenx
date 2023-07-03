from pymavlink import mavutil
import time
from enum import Enum

class ProgressStatus(Enum):
    OK = 0
    ERROR = 1

class MyMAVlink():
    def __init__(self,connection_id,baudrate) -> None:
        self.system_start_time = time.time()
        self.connection = mavutil.mavlink_connection(connection_id,baud=baudrate)
        self.target_system = self.connection.target_system
        self.target_component = self.connection.target_component

    def arm(self,data):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            data,0,0,0,0,0,0
        )
    def takeoff(self,data):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,0,0,0,0,0,data
        )
    def arm_and_takeoff(self,height,confirmation):
        self.arm(confirmation)
        self.takeoff(height)
    def move_forward(self,data):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,0,0,0,0,data,0
        )
    def change_position(self,data):
        #1=UP
        #0=DOWN
        type_mask = 3576
        x,y,z = data
        self.connection.mav.set_position_target_local_ned_send(
            int((time.time()-self.system_start_time)*1000),
            self.target_system,
            self.target_component,
            8,
            type_mask,
            x,y,z,
            0,0,0,
            0,0,0,
            0,0
        )
    def get_param(self):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,
            30,
            0, 0, 0, 0, 0, 0
        )

        while True:
            msg = self.connection.recv_match(type = "ATTITUDE", blocking = False)
            if not msg:
                continue
            else:
                print(msg.roll)
                break

    def get_gps(self):
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,
            33,
            0, 0, 0, 0, 0, 0
        )

        while True:
            msg = self.connection.recv_match(type = "GLOBAL_POSITION_INT", blocking = False)
            if not msg:
                continue
            else:
                print(msg)
                break
    
        