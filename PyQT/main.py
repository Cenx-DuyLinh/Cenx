import sys
from PyQt5.QtWidgets import *


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.window.setWindowTitle('My App')
        self.window.resize(1000, 1000)

        self.create_transit_frame()

        self.window.show()

    def create_transit_frame(self):
        self.frame_transit = QFrame(self.window)
        self.frame_transit.setFixedHeight(200)
        self.frame_transit.setFixedWidth(400)
        self.frame_transit.setFrameShape(QFrame.Box)
        self.frame_transit.move(100,100)
        self.layout_transit = QGridLayout(self.frame_transit)

        self.widget_folder_name = ['Arm','Guided', 'Take off','Set speed ','Transit 1-2-3','Transit 3-2-1','Takeoff Entry', 'Set Speed Entry', 'm','m/s' ]
        self.widget_folder_position = [0,0,
                                       0,1,
                                       1,0,
                                       1,1,
                                       3,0,
                                       3,1,
                                       2,0,
                                       2,1]
        self.widget_folder_command=[None]
        self.widget_name = {}

        for counter_buffer in range(len(self.widget_folder_name)):
            #Khi bỏ thêm widget thì nhớ chỉnh range của counter_buffer
            if counter_buffer in range(0,5+1):
                name_buffer = f'{self.widget_folder_name[counter_buffer]}'
                self.widget_name[name_buffer] = QToolButton(text=self.widget_folder_name[counter_buffer])
                self.widget_name[name_buffer].setFixedWidth(150)
                self.widget_name[name_buffer].setFixedHeight(40)
                self.layout_transit.addWidget(self.widget_name[name_buffer],self.widget_folder_position[counter_buffer*2],self.widget_folder_position[counter_buffer*2+1])
            elif counter_buffer in range(6,7+1):
                name_buffer = f'{self.widget_folder_name[counter_buffer]}'
                self.widget_name[name_buffer] = QLineEdit()
                self.widget_name[name_buffer].setFixedWidth(120)
                self.widget_name[name_buffer].setFixedHeight(30)
                self.layout_transit.addWidget(self.widget_name[name_buffer],self.widget_folder_position[counter_buffer*2],self.widget_folder_position[counter_buffer*2+1])
            elif counter_buffer == 8:
                name_buffer = self.widget_folder_name[counter_buffer]
                self.widget_name[name_buffer] = QLabel(name_buffer, parent=self.frame_transit)
                self.widget_name[name_buffer].setFixedWidth(20)
                self.widget_name[name_buffer].setFixedHeight(20)
                self.widget_name[name_buffer].move(160, 110)
            elif counter_buffer == 9:
                name_buffer = self.widget_folder_name[counter_buffer]
                self.widget_name[name_buffer] = QLabel(name_buffer, parent=self.frame_transit)
                self.widget_name[name_buffer].setFixedWidth(30)
                self.widget_name[name_buffer].setFixedHeight(20)
                self.widget_name[name_buffer].move(340, 110)

            

            




def RUN():
    app = QApplication(sys.argv)
    object_buffer = MyApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    RUN()