import socket
import time

# HOST = "127.0.0.1"
HOST = "10.8.0.62"
PORT = 1194

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")
    while True:
        data = s.recv(8192)
        message, timestamp = data.decode().split("\n")
        print(f"Received: {message}, Delay: {time.time() - float(timestamp)}s")
        time.sleep(0.1)
