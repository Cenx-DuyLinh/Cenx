import tkinter as tk

class MyTestApp:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.label_folder_name = ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5']
        self.label_folder_position = [0,0,   #Label 1 position
                                      0,1,   #Label 2 position
                                      1,0,   #Label 3 position
                                      1,1,   #Label 4 position 
                                      2,0]   #Label 5 position
        self.label_name = {}
        for counter in range(len(self.label_folder_name)):
            name_buffer = f"{self.label_folder_name[counter]}"
            self.label_name[name_buffer] = tk.Label(text = self.label_folder_name[counter])
            self.label_name[name_buffer].grid(row=self.label_folder_position[counter*2],column=self.label_folder_position[counter*2+1])
        self.window.mainloop()

test_object = MyTestApp()