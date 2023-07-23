from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from MAVlink_Test import MyMAVlink

class MainPage(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.MyCopter = MyMAVlink(connection_id= "tcp:127.0.0.1:5762", baudrate= 57600)
    def button_pressed(self):
        altitude = float(self.ids.input_text.text) 
        self.MyCopter.arm_and_takeoff(altitude, 1)

    pass
class DroneControlApp(App):
    pass

DroneControlApp().run()