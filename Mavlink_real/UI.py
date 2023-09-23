import tkinter as tk
from tkinter import font
from tkinter import messagebox
from MAVlink import MyMAVlink


class DroneControlApp:
    def __init__(self) -> None:
        self.MyCopter = MyMAVlink(
            connection_string="tcp:127.0.0.1:5762", baudrate=57600
        )
        self.window = tk.Tk()
        self.window.title("Drone Control App")

        # Customize font
        self.custom_font_title = font.Font(
            family="Tahoma", size=30, weight="bold", slant="italic"
        )
        self.custom_font_label = font.Font(underline=True, weight="bold")
        self.custom_font_drop = font.Font(family="Tahoma", size=18, weight="bold")
        self.custom_font_arrow = font.Font(size=18, weight="bold")

        self.label_title = tk.Label(
            master=self.window,
            text="Drone Control",
            font=self.custom_font_title,
            width=20,
        )
        self.label_title.grid(row=0, column=0, columnspan=2)

        self.create_search_frame()
        self.create_transit_frame()
        self.create_movement_frame()
        self.window.mainloop()

    def create_search_frame(self):
        self.frame_search = tk.Frame(
            self.window, borderwidth=1, relief="solid", width=300, height=350
        )
        self.frame_search.grid_propagate(False)
        self.frame_search.grid(row=1, column=1, padx=20, pady=20)

        button_width = 15
        button_heigth = 2

        def button_drop_warning():
            top = tk.Toplevel()
            top.title("WARNING!!")

            # Set the width and height of the dialog
            dialog_width = 300
            dialog_height = 170

            # Get the screen width and height
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()

            # Calculate the x and y coordinates of the top-left corner
            x = (screen_width - dialog_width) // 2
            y = (screen_height - dialog_height) // 2

            # Set the geometry of the dialog to position it in the center
            top.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

            label_warning = tk.Label(
                top, text="Do you want to drop the package ?", font="Arial 13"
            )
            label_warning.grid(row=0, column=0, columnspan=2, padx=15, pady=30)

            button_yes = tk.Button(
                top, text="Yes", command=lambda: (top.destroy()), width=10
            )
            button_yes.grid(row=1, column=0, columnspan=1)

            button_no = tk.Button(top, text="No", command=top.destroy, width=10)
            button_no.grid(row=1, column=1, columnspan=1)

        self.label_search = tk.Label(
            master=self.frame_search,
            text="Search Operation",
            font=self.custom_font_label,
        )
        self.button_cont = tk.Button(
            master=self.frame_search,
            text="Continue",
            width=button_width,
            height=button_heigth,
            command=lambda: self.MyCopter.mission_interaction(1),
        )
        self.button_stop = tk.Button(
            master=self.frame_search,
            text="Stop",
            width=button_width,
            height=button_heigth,
            command=lambda: self.MyCopter.mission_interaction(0),
        )
        self.button_takeGPS = tk.Button(
            master=self.frame_search,
            text="Take GPS",
            width=button_width,
            height=button_heigth,
            command=None,
        )
        self.button_RTH = tk.Button(
            master=self.frame_search,
            text="RTH",
            width=button_width,
            height=button_heigth,
            command=None,
        )
        self.button_drop = tk.Button(
            master=self.frame_search,
            text="DROP",
            font=self.custom_font_drop,
            width=15,
            height=2,
            bg="red",
            bd=5,
            command=button_drop_warning,
        )

        padx_button_search = 20
        pady_button_search = 10
        self.label_search.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.button_cont.grid(
            row=1, column=0, padx=padx_button_search, pady=pady_button_search
        )
        self.button_stop.grid(
            row=1, column=1, padx=padx_button_search, pady=pady_button_search
        )
        self.button_takeGPS.grid(
            row=2, column=0, padx=padx_button_search, pady=pady_button_search
        )
        self.button_RTH.grid(
            row=2, column=1, padx=padx_button_search, pady=pady_button_search
        )
        self.button_drop.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=padx_button_search,
            pady=pady_button_search,
        )

    def create_transit_frame(self):
        self.frame_transit = tk.Frame(
            self.window, borderwidth=1, relief="solid", width=300, height=350
        )
        self.frame_transit.grid_propagate(False)
        self.frame_transit.grid(row=1, column=0, padx=20, pady=20)

        button_width = 15
        button_heigth = 2
        entry_width = 5

        self.label_transit = tk.Label(
            master=self.frame_transit,
            text="Transit Operation",
            font=self.custom_font_label,
        )
        self.label_m = tk.Label(
            master=self.frame_transit,
            text="m                                               m/s",
        )
        self.button_arm = tk.Button(
            master=self.frame_transit,
            text="Arm & Takeoff",
            width=button_width,
            height=button_heigth,
            command=lambda: (
                self.MyCopter.arm_and_takeoff(float(self.entry_arm.get()))
            ),
        )
        self.button_setspeed = tk.Button(
            master=self.frame_transit,
            text="Set Speed",
            width=button_width,
            height=button_heigth,
            command=None,
        )
        self.button_123 = tk.Button(
            master=self.frame_transit,
            text="Enter transit 1-2-3",
            width=button_width,
            height=button_heigth,
            command=None,
        )
        self.button_321 = tk.Button(
            master=self.frame_transit,
            text="Exit transit 3-2-1",
            width=button_width,
            height=button_heigth,
            command=None,
        )
        self.button_land = tk.Button(
            master=self.frame_transit,
            text="Land Drone",
            width=button_width,
            height=button_heigth,
            command=None,
        )

        self.entry_setspeed = tk.Entry(
            master=self.frame_transit, width=entry_width, font="Arial 18"
        )
        self.entry_arm = tk.Entry(
            master=self.frame_transit, width=entry_width, font="Arial 18"
        )

        padx_button_transit = 20
        pady_button_transit = 20
        self.label_transit.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=padx_button_transit,
            pady=pady_button_transit,
        )
        self.button_arm.grid(
            row=1, column=0, padx=padx_button_transit, pady=pady_button_transit
        )
        self.button_setspeed.grid(
            row=1, column=1, padx=padx_button_transit, pady=pady_button_transit
        )
        self.button_123.grid(
            row=3, column=0, padx=padx_button_transit, pady=pady_button_transit
        )
        self.button_321.grid(
            row=3, column=1, padx=padx_button_transit, pady=pady_button_transit
        )

        padx_entry = 20
        pady_entry = 1
        self.entry_arm.grid(row=2, column=0, padx=padx_entry, pady=pady_entry)
        self.entry_setspeed.grid(row=2, column=1, padx=padx_entry, pady=pady_entry)

    def create_movement_frame(self):
        self.frame_movement = tk.Frame(
            self.window, borderwidth=1, relief="solid", width=650, height=300
        )
        self.frame_movement.grid_propagate(False)
        self.frame_movement.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 50))

        # Create component
        self.label_movement = tk.Label(
            master=self.frame_movement,
            text="Drone Movement",
            font=self.custom_font_label,
        )
        self.label_DistantToMove = tk.Label(
            master=self.frame_movement,
            text="Distant to move:                  m",
            font="Arial 13",
        )
        self.label_AltitudeToMove = tk.Label(
            master=self.frame_movement,
            text="Altitude to move:                  m",
            font="Arial 13",
        )
        self.button_forward = tk.Button(
            master=self.frame_movement,
            text="↑",
            font=self.custom_font_arrow,
            width=3,
            height=1,
            bd=3,
            command=None,
        )
        self.button_backward = tk.Button(
            master=self.frame_movement,
            text="↓",
            font=self.custom_font_arrow,
            width=3,
            height=1,
            bd=3,
            command=None,
        )
        self.button_left = tk.Button(
            master=self.frame_movement,
            text="←",
            font=self.custom_font_arrow,
            width=3,
            height=1,
            bd=3,
            command=None,
        )
        self.button_right = tk.Button(
            master=self.frame_movement,
            text="→",
            font=self.custom_font_arrow,
            width=3,
            height=1,
            bd=3,
            command=None,
        )
        self.button_up = tk.Button(
            master=self.frame_movement,
            text="Up",
            font=self.custom_font_arrow,
            width=6,
            height=2,
            bd=3,
            command=None,
        )
        self.button_down = tk.Button(
            master=self.frame_movement,
            text="Down",
            font=self.custom_font_arrow,
            width=6,
            height=2,
            bd=3,
            command=None,
        )
        self.entry_DistantToMove = tk.Entry(
            master=self.frame_movement, width=8, font="arial 13"
        )
        self.entry_AltitudeToMove = tk.Entry(
            master=self.frame_movement, width=8, font="arial 13"
        )

        # Place component
        self.label_movement.place(x=250, y=20)
        self.label_DistantToMove.place(x=40, y=250)
        self.entry_DistantToMove.place(x=40 + 130, y=250)
        self.label_AltitudeToMove.place(x=400, y=250)
        self.entry_AltitudeToMove.place(x=400 + 130, y=250)
        self.button_forward.place(x=111, y=50)
        self.button_backward.place(x=111, y=160)
        self.button_left.place(x=55, y=105)
        self.button_right.place(x=165, y=105)
        self.button_up.place(x=450, y=50)
        self.button_down.place(x=450, y=140)

        pass


def RUN():
    object = DroneControlApp()


if __name__ == "__main__":
    RUN()
