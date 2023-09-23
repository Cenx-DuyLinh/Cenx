import socket
import time
import ast


# HOST = "10.8.0.13"
HOST = "127.0.0.1"
PORT = 1194

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")
    while True:
        data = s.recv(1024)
        data = data.decode()
        list_ = ast.literal_eval(data)
        print(list_)
        print(type(list_))
        print(f"Received:, {list_[0]}, Delay: {time.time() - list_[1]}s")
        time.sleep(0.1)
