import tkinter as tk 
from UI_Test import DroneControlApp
class TestDroneParameter:
    def __init__(self) -> None:
        self.window_buffer = tk.Tk()
        self.window_buffer.withdraw()
        self.window1 = DroneControlApp()
        #self.window1.window.geometry('100+100')
        self.window2 = tk.Toplevel()
        self.window2.geometry('300x100+400+100')
        self.create_label()
        self.window2.mainloop()
    def create_label(self):
        self.label_folder_name = ['Pitch','Roll','Yaw','Altitude'] 
        self.label_folder_position = [0,0,
                                      0,1,
                                      0,2,
                                      0,3,]
        self.label_name = {}
        for counter in range(len(self.label_folder_name)):
            name_buffer = f"{self.label_folder_name[counter]}"
            self.label_name[name_buffer] = tk.Label(master=self.window2,text = self.label_folder_name[counter])
            self.label_name[name_buffer].grid(row=self.label_folder_position[counter*2],column=self.label_folder_position[counter*2+1])

def RUN():
    object = TestDroneParameter()
if __name__ == "__main__":
    RUN()



