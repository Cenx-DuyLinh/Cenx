from abc import ABC, abstractmethod
from enum import Enum
from pymavlink import mavutil
import os
import datetime
import time
import threading
import logging
import logging.config
import logging.handlers
import timeit
import queue
import sys

class ProgressStatus(Enum):
    OK = 0
    ERROR = 1
    PPM_CONTROL_ON = 3

class StatusDataFlag:
    def __init__(self):
        self.mavlink_communication_error = False
        self.ai_communication_error = False
        self.ppm_control_ch_on = False

    def set_mavlink_communication_error(self, value:bool):
        self.mavlink_communication_error = value

    def set_ai_communication_error(self, value:bool):
        self.ai_communication_error = value

    def set_ppm_control_ch(self, value:bool):
        self.ppm_control_ch_on = value

    def is_mavlink_communication_error(self) -> bool:
        return self.mavlink_communication_error

    def is_ai_communication_error(self) -> bool:
        return self.ai_communication_error
    
    def is_ppm_control_ch_on(self) -> bool:
        return self.ppm_control_ch_on
    
class LoggingManager:
    def __init__(self):
        self.loggers = {}
        self.log_file = self.get_log_file()
        
    def get_log_file(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(log_dir, f"{current_time}.log")

    def setup_logger(self, obj):
        obj_id = id(obj)
        #convert the object id to string
        obj_id = str(obj_id)
        obj_logger = self.create_logger(obj_id)
        self.loggers[obj_id] = obj_logger

    def create_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def get_logger(self, obj):
        obj_id = id(obj)
        return self.loggers.get(obj_id, None)

    def log_info(self, obj, message):
        logger = self.get_logger(obj)
        if logger is not None:
            logger.info(message)
            
class SettingFile:
    def __init__(self):
        self.sensor_frequency = None
        self.ai_data_frequency = None
        self.default_logging_frequency = None
        self.output_frequency = None
        self.stand_modert_log_frequency = None
        self.ai_host = None
        self.ai_host_port = None
        self.ch_control_number = None
        self.ardupilot_connection_string = None
        self.uav_type = None
        #get current path to pathvalue
        self.pathvalue = os.path.dirname(os.path.abspath(__file__))
        self.path =  os.path.join(self.pathvalue, "setting.init")
        try :
            config_file_path = self.read_setting_file( os.path.join(self.pathvalue, "setting.init"))
            #define path + setting.init   
        except Exception as e:
            self.gen_file(self.pathvalue)
            self.read_setting_file( os.path.join(self.pathvalue, "setting.init"))

    def read_setting_file(self, file_path):
        # implementation details for reading setting file
        with open(file_path) as f:
            for line in f:
                key, value = line.strip().split('=')
                if key == 'SensorFrequency':
                    self.sensor_frequency = int(value)
                elif key == 'AIDataFrequency':
                    self.ai_data_frequency = int(value)
                elif key == 'DefaultLoggingFrequency':
                    self.default_logging_frequency = int(value)
                elif key == 'OutputFrequency':
                    self.output_frequency = int(value)
                elif key == 'AIHost':
                    self.ai_host = value
                elif key == 'AIHostPort':
                    self.ai_host_port = int(value)
                elif key == 'CHControlNumber':
                    self.ch_control_number = int(value)
                elif key == 'ArdupilotConnectionString':
                    self.ardupilot_connection_string = value
                elif key == 'UAVType':
                    self.uav_type = value
                else:
                    raise ValueError(f"Invalid key in setting file: {key}")

    def gen_file(self, file_path):
        default_settings = {
            'SensorFrequency': '1',
            'DefaultLoggingFrequency': '1',
            'AIDataFrequency': '1',
            'OutputFrequency': '1',
            'AIHost': 'localhost',
            'AIHostPort': '50051',
            'CHControlNumber': '7',
            'ArdupilotConnectionString': 'udp:127.0.0.1:14551',
            'UAVType': 'quadcopter'
        }
        filename = f"setting.init"
        with open(os.path.join(file_path, filename), 'w') as f:
            for key, value in default_settings.items():
                f.write(f"{key}={value}\n")
        self.read_setting_file(os.path.join(file_path, filename))

    def get_sensor_frequency(self):
        return self.sensor_frequency

    def get_default_logging_frequency(self):
        return self.default_logging_frequency

    def get_ai_data_frequency(self):
        return self.ai_data_frequency
    
    def get_output_frequency(self):
        return self.output_frequency

    def get_stand_modert_log_frequency(self):
        return self.stand_modert_log_frequency

    def get_ai_host(self):
        return self.ai_host

    def get_ai_host_port(self):
        return self.ai_host_port

    def get_ch_control_number(self):
        return self.ch_control_number

    def get_ardupilot_connection_string(self):
        return self.ardupilot_connection_string

    def get_uav_type(self):
        return self.uav_type

class AIData:
    def __init__(self):
        pass

class MAVLinkCommandCode(Enum):
    ARM_DISARM = 0
    GUIDED_MODE = 1
    SET_ALTITUDE = 2
    SET_FRAME_POSITION = 3
    SET_GPS_POSITION = 4
    SET_SPEED = 5
    SET_SERVO = 6
    FAILSAFE = 7
    GET_PARAM = 8
    GET_DATA = 9
    TAKE_OFF = 10
    RETURN_TO_LAND = 11
    SET_FRAME_VELOCITY = 12
    OVERRIDE_CHANNEL = 13
    
class MAVLinkDataType(Enum):
    PARAM = 0
    ALTITUDE = 1
    GPS_LOCATION = 2
    FRAME_LOCATION = 3
    VELOCITY = 4
    MODE = 5
    SERVO = 6
    CHANNEL_PWM = 7
    SPEEDTYPE_SPEED = 8
    
class MAVLinkData:
    pass

class MAVLink:
    def __init__(self, setting_file):
        connection_string = setting_file.get_ardupilot_connection_string()
        self.rc_control_channel = setting_file.get_ch_control_number()
        self.uav_type = setting_file.get_uav_type()
        self.error_flag = False
        self.connection = mavutil.mavlink_connection(connection_string, baud =57600)
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
        else: return ProgressStatus.ERROR

    def update(self, command_code: MAVLinkCommandCode, data_type: MAVLinkDataType, data) -> ProgressStatus:
        self.command_code = command_code
        self.data_type = data_type
        self.data = data
        return ProgressStatus.OK
    
    def send(self) -> ProgressStatus:
        try:
            if self.command_code == MAVLinkCommandCode.ARM_DISARM:
                self.arm_disarm(self.data)

            # elif self.command_code == MAVLinkCommandCode.GUIDED_MODE:
            #     self.guided_mode()
            
            # elif self.command_code == MAVLinkCommandCode.SET_ALTITUDE:
            #     self.set_altitude(self.data)
            
            elif self.command_code == MAVLinkCommandCode.SET_FRAME_POSITION:
                self.set_frame_position(self.data)

            elif self.command_code == MAVLinkCommandCode.SET_FRAME_VELOCITY:
                self.set_frame_velocity(self.data)

            elif self.command_code == MAVLinkCommandCode.SET_GPS_POSITION:
                self.set_gps_position(self.data)
            
            elif self.command_code == MAVLinkCommandCode.SET_SPEED:
                self.set_speed(self.data)
            
            elif self.command_code == MAVLinkCommandCode.SET_SERVO:
                self.set_servo(self.data)
            
            elif self.command_code == MAVLinkCommandCode.TAKE_OFF:
                self.take_off(self.data)
            
            elif self.command_code == MAVLinkCommandCode.RETURN_TO_LAND:
                self.return_to_land()
            
            elif self.command_code == MAVLinkCommandCode.FAILSAFE:
                self.failsafe()
            
            elif self.command_code == MAVLinkCommandCode.GET_PARAM:
                self.get_all_params()
            
            elif self.command_code == MAVLinkCommandCode.OVERRIDE_CHANNEL:
                self.rc_channel_override(self.data)
            
            return ProgressStatus.OK
        except:
            self.error_flag = True
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
    
    # def take_off_sequence(self, altitude):
    #     self.arm_disarm(1)
    #     time.sleep(5)
    #     self.take_off(altitude)
    #     time.sleep(int(altitude/2))
    
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
     
    # def guided_mode(self):
    #     self.connection.mav.command_long_send(
    #         self.target_system,
    #         self.target_component,
    #         mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    #         0,
    #         1,
    #         4, 0, 0, 0, 0, 0
    #     )
    
    # def set_altitude(self, data):
    #     altitude = data
    #     self.connection.mav.command_long_send(
    #         self.target_system,
    #         self.target_component,
    #         mavutil.mavlink.MAV_CMD_DO_CHANGE_ALTITUDE,
    #         0,
    #         altitude,
    #         3,0,0,0,0,0
    #     )
    
    def set_frame_position(self, data):
        #Copter:
            #Use Position : 0b110111111000 / 0x0DF8 / 3576 (decimal)
            #Use Velocity : 0b110111000111 / 0x0DC7 / 3527 (decimal)
            #Use Acceleration : 0b110000111111 / 0x0C3F / 3135 (decimal)
            #Use Pos+Vel : 0b110111000000 / 0x0DC0 / 3520 (decimal)
            #Use Pos+Vel+Accel : 0b110000000000 / 0x0C00 / 3072 (decimal)
            #Use Yaw : 0b100111111111 / 0x09FF / 2559 (decimal)
            #Use Yaw Rate : 0b010111111111 / 0x05FF / 1535 (decimal)
            
        #Rover
            #Use Position : 0b110111111100 / 0x0DFC / 3580 (decimal)
            #Use Velocity : 0b110111100111 / 0x0DE7 / 3559 (decimal)
            #Use Yaw : 0b100111111111 / 0x09FF / 2559 (decimal)
            #Use Yaw Rate : 0b010111111111 / 0x05FF / 1535 (decimal)
            #Use Vel+Yaw : 0b100111100111 / 0x09E7 / 2535 (decimal)
            #Use Vel+Yaw Rate : 0b010111100111 / 0x05E7 / 1511 (decimal)

        if self.uav_type == 'quadcopter':
            type_mask = 3576
        else: #'rover'
            type_mask = 3580
        
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
    
    def set_frame_velocity(self, data):
        if self.uav_type == 'quadcopter':
            type_mask = 3527
        else: #'rover'
            type_mask = 3559
        
        vx, vy, vz = data
        self.connection.mav.set_position_target_local_ned_send(
            int(1e3 * (time.time() - self.boot_time)),          #time_boot_ms
            self.target_system,
            self.target_component,       #target_system, taget_component
            8, #frame valid options are: MAV_FRAME_LOCAL_NED = 1, MAV_FRAME_LOCAL_OFFSET_NED = 7, MAV_FRAME_BODY_NED = 8, MAV_FRAME_BODY_OFFSET_NED = 9
            type_mask,       #type_mask (only position)
            0, 0, 0,    #x, y, z positions in m
            vx, vy, vz,    #vy, vy, vz velocity in m/s
            0, 0, 0,    #ax, ay, az acceleration
            0, 0        #yaw, yaw_rate
        )
        
    def set_gps_position(self, data):
        #MAV_FRAME_GLOBAL (0): alt is meters above sea level
        #MAV_FRAME_GLOBAL_INT (5): alt is meters above sea level
        #MAV_FRAME_GLOBAL_RELATIVE_ALT (3): alt is meters above home
        #MAV_FRAME_GLOBAL_RELATIVE_ALT_INT (6): alt is meters above home
        #MAV_FRAME_GLOBAL_TERRAIN_ALT (10): alt is meters above terrain
        #MAV_FRAME_GLOBAL_TERRAIN_ALT_INT (11): alt is meters above terrain
        
        #int(latitude and longitude * 1e7)
        latitude, longitude, altitude = data
        self.connection.mav.set_position_target_global_int_send(
            int(1e3 * (time.time() - self.boot_time)),
            self.target_system,
            self.target_component,
            6,
            3576,
            latitude,
            longitude,
            altitude,
            0, 0, 0,    #vy, vy, vz velocity in m/s
            0, 0, 0,    #ax, ay, az acceleration
            0, 0        #yaw, yaw_rate
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
    
    def get_rc_control_channel(self):
        try:
            while True:
                message = self.connection.recv_match(type = "RC_CHANNELS", blocking = False)
                if message != None:
                    control_channel_value = eval(f'message.chan{self.rc_control_channel}_raw')
                    return control_channel_value
        except Exception as e:
            print(e)
    
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
        
    def set_servo(self, data):
        channel, pwm = data
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,
            channel,
            pwm,
            0,0,0,0,0
        )
    
    def get_all_params(self):
        self.connection.param_fetch_all()
        while True:
            try:
                message = self.connection.recv_match(type='PARAM_VALUE', blocking = False)
                print(message.param_id, message.param_value)
            except Exception as e:
                print(e)
                sys.exit(0)
                    
    def get_attitude(self):
        try:
            message = self.connection.recv_match(type = "ATTITUDE", blocking = False)
            if message != None:
                return message
        except Exception as e:
            print(e)
    
    def get_altitude(self):
        try:
            message =  self.connection.recv_match(type = "GLOBAL_POSITION_INT", blocking = False)
            if message != None:
                return message.alt
        except Exception as e:
            print(e)
            
    def failsafe(self):
        try:
            print("Return to land")
            self.connection.set_mode_rtl()
        except Exception as e:
            print(e)
            print("Can not set mode RTL")

    def check_mavlink_is_error(self):
        return self.error_flag

class UAVConcept(ABC):
    
    @abstractmethod
    def GetDataFromArdupilot(self) -> tuple[ProgressStatus, MAVLinkData, bool]:
        """
        This abstract method is meant to be implemented by a subclass of UAVConcept.
        The method should retrieve data from the Ardupilot, including communication status and PPM control status.

        Returns:
            tuple[StatusData, MAVLinkCommunication, StatusData]: A tuple containing the following elements:
                - Communication status (StatusData): An instance of StatusData class representing the communication status.
                - MAVLinkCommunication: An instance of a class containing the received MAVLink data.
                - PPM control status (bool): A boolean value indicating whether the PPM control is enabled.
        """
        pass
    
    # @abstractmethod
    # def UAVRun(self):
    #     pass
    
    @abstractmethod
    def GetAIData(self)-> tuple[ProgressStatus,AIData]:
        pass
    
    @abstractmethod
    def Ardupilot_init(self)-> ProgressStatus:
        pass
    
    @abstractmethod
    def CalulationOutput(self,SubSettingFileInfor,AIData,MAVLinkData)-> tuple[ProgressStatus,MAVLinkData]:
        pass
    
    @abstractmethod
    def SendOutputcommand(self, CommandData, StatusData:StatusDataFlag) -> ProgressStatus:
        pass
    
    def __init__(self, setting_file):
        #Step 0:[Init]use setting file infor to init all infor
        self.SettingFileInfor = setting_file
        # Register the handler for the SIGALRM signal
            # Register the handler for the SIGALRM signal
        self.AIDataInfor = AIData()
        self.OutputData = tuple[ProgressStatus,MAVLinkData]
        self.MainToSubQueueForAI = queue.Queue()
        self.MainToSubQueueForMAVLink = queue.Queue()
        self.MaintoSubQueueStatus = queue.Queue()
        self.SubToMainQueueForOutput = queue.Queue()
        self.logging_manager = LoggingManager()
        #Step 1:[Init]use pymavlink.mavutil to connect to ardupilot by setting file infor
        try:
            self.CurrentStatusData = self.Ardupilot_init()
        except Exception as e:
            print(f"Error connecting to device: {e}")
            exit()
        pass

    def PutSysnchronizeOutputDataFromSubToMain(self,Data:MAVLinkData):
        #clear all data in queue 
        while not self.SubToMainQueueForOutput.empty():
            self.SubToMainQueueForOutput.get()
        #put data to main thread
        self.SubToMainQueueForOutput.put(Data)
        pass
    
    def timeout_handler(self, frame):
        raise TimeoutError("Operation timed out")
  
    def GetSysnchronizeOutputDataFromSubToMain(self):
        if not self.SubToMainQueueForOutput.empty():
            Data = self.SubToMainQueueForOutput.get_nowait()
            successfullyProcessed = ProgressStatus
            # create tuple
            return ProgressStatus.OK, Data
        else :
            return ProgressStatus.ERROR, None
            
    def OutputCaclulatorThread(self, SettingFileInfor:SettingFile)-> StatusDataFlag :
        #[Sub Thread] process
        SubSettingFileInfor = SettingFileInfor
        SubStatusDataInfor = StatusDataFlag()
        MAVLinkData = None
        AIdata = None
        mavlink_updated = False
        data_updated = False
        while True:
            try:
                # Get the latest data from the main thread
                while not self.MainToSubQueueForAI.empty():
                    AIdata = self.MainToSubQueueForAI.get_nowait()

                while not self.MainToSubQueueForMAVLink.empty():
                    MAVLinkData = self.MainToSubQueueForMAVLink.get_nowait()
                    mavlink_updated = True
                    #data_updated = True

                while not self.MaintoSubQueueStatus.empty():
                    SubStatusDataInfor = self.MaintoSubQueueStatus.get_nowait()
                    if mavlink_updated:
                        data_updated = True
                        mavlink_updated = False
                    
            except:
                # Continue the loop if any of the queues are empty
                print ("Error")
                pass
            
            # self.mavlink_communication_error = False
            # self.ai_communication_error = False
            #  self.ppm_control_ch_on = False
            # If there is an AI communication error, enter failsafe progress run
            
            if SubStatusDataInfor.ai_communication_error:
                # TODO:  Code for handling failsafe progress run goes here
                pass
            
            # If there is an Ardupilot communication error, enter failsafe progress run
            elif SubStatusDataInfor.mavlink_communication_error:
                # TODO: Code for handling failsafe progress run goes here
                pass

            #data_updated = True and  and SubStatusDataInfor.mavlink_communication_error == False and SubStatusDataInfor.ai_communication_error == False and SubStatusDataInfor.PPM_control_error == true
            if data_updated == True and SubStatusDataInfor.mavlink_communication_error == False and SubStatusDataInfor.ai_communication_error == False and SubStatusDataInfor.ppm_control_ch_on == True:
                    # If status is OK
                    OutputData = self.CalulationOutput(SubSettingFileInfor, AIdata, MAVLinkData)[1]
                    self.PutSysnchronizeOutputDataFromSubToMain(OutputData)
                    OutputData = None
                    data_updated = False
                    pass
                
            else:
                # data_updated value 
                # print("data_updated value is ",data_updated)
                # # print SubStatusDataInfor.mavlink_communication_error 
                # print("SubStatusDataInfor.mavlink_communication_error value is ",SubStatusDataInfor.mavlink_communication_error)
                # #print SubStatusDataInfor.ai_communication_error 
                # print("SubStatusDataInfor.ai_communication_error value is ",SubStatusDataInfor.ai_communication_error)
                pass

    def start(self, log:LoggingManager):
        self.logging_manager= log
        #[Main thread] progress
        self.SubThread = threading.Thread(target=self.OutputCaclulatorThread, args=(self.SettingFileInfor,))
        self.SubThread.start()
        default_logger = self.logging_manager.get_logger("default")
        default_logging_frequency = self.SettingFileInfor.get_default_logging_frequency()
        ai_frequency = self.SettingFileInfor.get_ai_data_frequency()  # get AI data frequency from setting file
        ai_interval = 1e6 / ai_frequency  # calculate interval between AI data reads (in microseconds)
        ardupilot_frequency = self.SettingFileInfor.get_sensor_frequency()  # get sensor data frequency from setting file
        ardupilot_interval = 1e6 / ardupilot_frequency  # calculate interval between sensor data reads (in microseconds)
        output_frequency = self.SettingFileInfor.get_output_frequency()  # get output frequency from setting file
        output_interval = 1e6 / output_frequency  # calculate interval between output data reads (in microseconds)
        logging_frequency = self.SettingFileInfor.get_default_logging_frequency()  # get logging frequency from setting file
        logging_interval = 1e6 / logging_frequency  # calculate interval between logging data reads (in microseconds)
        error_counter = 0
        ai_elapsed_time = 0
        ardupilot_elapsed_time = 0
        output_elapsed_time = 0
        logging_elapsed_time = 0
        start_time = timeit.default_timer()  # get current time in microseconds
        
        while True:
            try:
                self.CurrentStatusData = StatusDataFlag()
                current_time = datetime.datetime.now()
                
                #1 [AI Data]Get AI data if current time is within the interval
                if ai_elapsed_time >= ai_interval:
                    SetData = self.GetAIData()
                    if SetData[0] == ProgressStatus.OK:
                        self.MainToSubQueueForAI.put(SetData[1])
                        self.CurrentStatusData.ai_communication_error = False
                    else:
                        self.MainToSubQueueForAI.put(None)
                        self.CurrentStatusData.ai_communication_error = True
                    #update status
                    self.MaintoSubQueueStatus.put(self.CurrentStatusData)
                    ai_elapsed_time = 0
                        
                #2 [Ardupilot Data]Get data from Ardupilot IF current time is within the interval          
                if ardupilot_elapsed_time >= ardupilot_interval:
                    SetData = self.GetDataFromArdupilot()
                    if SetData[0] == ProgressStatus.OK:
                        self.MainToSubQueueForMAVLink.put(SetData[1])
                        self.CurrentStatusData.mavlink_communication_error = False
                        # Update PPM control channel status based on Ardupilot data
                        self.CurrentStatusData.ppm_control_ch_on=SetData[2]
                    else:
                        self.MainToSubQueueForMAVLink.put(None)
                        self.CurrentStatusData.mavlink_communication_error = True
                        # Update PPM control channel status based on Ardupilot data
                        self.CurrentStatusData.ppm_control_ch_on= False
                    pass
                    #if self.CurrentStatusData notype error
                    if self.CurrentStatusData is None:
                        pass
                    #update status
                    self.MaintoSubQueueStatus.put(self.CurrentStatusData)
                    ardupilot_elapsed_time = 0
                    pass
                pass
            
                #3 [Output Data] send output command to Ardupilot if within the interval and no communication errors
                if output_elapsed_time >= output_interval:
                    Progressstatus, self.OutputData = self.GetSysnchronizeOutputDataFromSubToMain()
                    if  self.CurrentStatusData.mavlink_communication_error == False and self.CurrentStatusData.ai_communication_error == False and self.CurrentStatusData.ppm_control_ch_on == True and Progressstatus == ProgressStatus.OK:
                            self.CurrentStatusData = self.SendOutputcommand(self.OutputData,self.CurrentStatusData )
                            #delete output data
                            self.OutputData = None
                            
                    output_elapsed_time = 0
                    pass
                pass
            
                #4 [Logging Data] log data if within the interval
                if logging_elapsed_time >= logging_interval:
                    #TODO: log data
                    logging_elapsed_time = 0
                    pass
                
                # Calculate the time elapsed during the operations
                current_time = timeit.default_timer()
                elapsed_time = (current_time-start_time) * 1000000
                start_time =  current_time
                
                # elapsed_time =elapsed_time/1e6
                
                # Update elapsed time for all operations
                ai_elapsed_time += elapsed_time
                ardupilot_elapsed_time += elapsed_time
                output_elapsed_time += elapsed_time
                logging_elapsed_time += elapsed_time
                
                # Calculate the remaining time in the interval for each operation
                ai_sleep_time = ai_interval - ai_elapsed_time
                ardupilot_sleep_time = ardupilot_interval - ardupilot_elapsed_time
                output_sleep_time = output_interval - output_elapsed_time
                logging_sleep_time = logging_interval - logging_elapsed_time
                
                # Sleep for the minimum remaining time in the interval, if any
                min_sleep_time = min(ai_sleep_time, ardupilot_sleep_time, output_sleep_time, logging_sleep_time)
                if min_sleep_time > 0:
                    #convert min_sleep_time to int
                    min_sleep_time_int = min_sleep_time/1e6
                    time.sleep(min_sleep_time_int)
                    pass
                pass
            
            except Exception as ex:
                print(f"An error occurred: {ex}")
                error_counter += 1
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1 / default_logging_frequency:
                    #default_logger.error(f"An error occurred: {ex}")
                    #TODO: Note the error into log file
                    error_counter = 0
                    start_time = time.time()
                    pass