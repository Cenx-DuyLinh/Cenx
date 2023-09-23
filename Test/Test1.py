from pymavlink import mavutil
import tkinter as tk
import time

# from ArdupilotControlApp.Master.UAVConcept import *
from enum import Enum


class ProgressStatus(Enum):
    OK = 0
    ERROR = 1


class LinhRover:
    def __init__(self, connection_id, baudrate) -> None:
        self.system_start_time = time.time()
        self.connection = mavutil.mavlink_connection(connection_id, baudrate)
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
                int(time.time() * 1e6),  # Unix time in microseconds
                0,  # Ping number
                0,  # Request ping of all systems
                0,  # Request ping of all components
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

    def rc_channel_override(self, data):
        channels, pwms = data
        rc_channel_value = [65535 for _ in range(8)]
        for i in range(len(channels)):
            rc_channel_value[channels[i] - 1] = pwms[i]

        self.connection.mav.rc_channels_override_send(
            self.target_system, self.target_component, *rc_channel_value
        )

    def get_pwm_output(self, data):
        channel = data
        self.connection.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
            0,
            36,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        if channel == 1:
            counter = 5
            while counter <= 10:
                message = self.connection.recv_match(
                    type="SERVO_OUTPUT_RAW", blocking=True
                )  # Filter for SERVO_OUTPUT_RAW messages
                if message is not None:
                    servo_pwm1 = message.servo1_raw
                    servo_pwm2 = message.servo2_raw
                    servo_pwm3 = message.servo3_raw
                    print(f"Servo 1 PWM value: {servo_pwm1}")
                    print(f"Servo 2 PWM value: {servo_pwm2}")
                    print(f"Servo 3 PWM value: {servo_pwm3}")
                counter = counter + 0.2
                time.sleep(0.2)


class LinhUI:
    def __init__(self):
        # self.connection = LinhRover(connection_id='udp::14552')
        self.connection = LinhRover(connection_id="COM7", baudrate=57600)
        # Nhớ cho thêm baudrate
        # self.connection = 1
        self.window = tk.Tk()
        self.create_buttons()
        self.run()

    def create_buttons(self):
        # Left
        left_button = tk.Button(
            self.window,
            text="LEFT",
            font=("Arial", 24),
            command=lambda: self.move_left(),
        )
        left_button.pack(side=tk.LEFT)

        # Neutral
        neutral_button1 = tk.Button(
            self.window,
            text="MID",
            font=("Arial", 24),
            command=lambda: self.move_neutral_lr(),
        )
        neutral_button1.pack(side=tk.LEFT)

        # Right
        right_button = tk.Button(
            self.window,
            text="RIGHT",
            font=("Arial", 24),
            command=lambda: self.move_right(),
        )
        right_button.pack(side=tk.LEFT)

        # Up
        up_button = tk.Button(
            self.window, text="UP", font=("Arial", 24), command=lambda: self.move_up()
        )
        up_button.pack(side=tk.TOP)

        # Neutral
        neutral_button2 = tk.Button(
            self.window, text="MID", font=("Arial", 24), command=self.move_neutral_ud
        )
        neutral_button2.pack(side=tk.TOP)

        # Down
        down_button = tk.Button(
            self.window, text="DOWN", font=("Arial", 24), command=self.move_down
        )
        down_button.pack(side=tk.TOP)

        # PWM
        pwm_button = tk.Button(
            self.window,
            text="PWM",
            font=("Arial", 24),
            command=lambda: self.get_pwm_values(),
        )
        pwm_button.pack(side=tk.BOTTOM)

    def move_left(self):
        self.connection.rc_channel_override([[1, 2, 3], [1700, 0, 0]])

    def move_right(self):
        self.connection.rc_channel_override([[1, 2, 3], [1200, 0, 0]])

    def move_up(self):
        self.connection.rc_channel_override([[1, 2, 3], [0, 0, 1600]])

    def move_down(self):
        self.connection.rc_channel_override([[1, 2, 3], [0, 0, 1400]])

    def move_neutral_lr(self):
        self.connection.rc_channel_override([[1, 2, 3], [1500, 0, 0]])

    def move_neutral_ud(self):
        self.connection.rc_channel_override([[1, 2, 3], [0, 0, 1500]])

    def get_pwm_values(self):
        pwm_value = self.connection.get_pwm_output(1)

    def run(self):
        self.window.mainloop()


def RUN():
    object = LinhUI()


if __name__ == "__main__":
    RUN()
