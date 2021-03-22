import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "exit"
SERVER = "SERVER_IP"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def msg_to_server():
    while True:
        msg = input()
        client.send(msg.encode(FORMAT))
        if msg == DISCONNECT_MESSAGE:
            client.close()


def server_scan():  # сканнер серверных сообщений
    while True:
        msg = client.recv(HEADER).decode(FORMAT)
        print("[SERVER] " + msg)


def start():
    thread = threading.Thread(target=server_scan)
    thread.start()
    msg_to_server()


start()