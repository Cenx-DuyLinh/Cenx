import socket
import time
import tkinter as tk


class Sever:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.listen()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Listening")
            self.conn, addr = s.accept()
            print(f"Con: {self.conn}, Address: {addr}")
            self.build_app()

    def send_message(self):
        message = ["djtconmemay", time.time()]
        message_encode = str(message).encode()
        self.conn.sendall(message_encode)

    def build_app(self):
        app = tk.Tk()
        frame = tk.Frame(
            master=app,
            width=640,
            height=480,
            highlightthickness=1,
            highlightbackground="black",
        )
        frame.pack()

        button = tk.Button(master=frame, text="UP", command=lambda: self.send_message())
        button.pack()
        button2 = tk.Button(
            master=frame, text="UP", command=lambda: self.send_message()
        )
        button2.pack()
        button3 = tk.Button(
            master=frame, text="UP", command=lambda: self.send_message()
        )
        button3.pack()
        button4 = tk.Button(
            master=frame, text="UP", command=lambda: self.send_message()
        )
        button4.pack()

        app.mainloop()


def RUN():
    HOST = "10.8.0.13"
    # HOST = "127.0.0.1"
    PORT = 1194
    object_sever = Sever(HOST, PORT)


if __name__ == "__main__":
    RUN()
