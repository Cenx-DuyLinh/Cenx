from PIL import Image, ImageTk
import tkinter as tk

# Create a Tkinter window
window = tk.Tk()

# Open the image using PIL
image = Image.open("logo_bk.png")

# Convert the image to a Tkinter-compatible format
tkimage = ImageTk.PhotoImage(image)

# Create a Tkinter label and display the image
label = tk.Label(window, image=tkimage)
label.pack()

# Run the Tkinter event loop
window.mainloop()