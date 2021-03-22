import socket
import threading

HEADER = 64  # сколько байтов может содержать сообщение
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "exit"
CONNECTED_LIST = []
CONN_LIST = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создание сокет объекта
server.bind(ADDR)  # биндим сервер и порт


def handle_client(conn, addr):  # функция работы сервера с клиентом
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg = conn.recv(HEADER).decode(FORMAT)
            if msg:  # если получает от клиента сообщение то обрабатывает его по шаблонам
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    del CONN_LIST[CONN_LIST.index(conn)]
                    del CONNECTED_LIST[CONNECTED_LIST.index(addr)]
                print(f"[{addr}] {msg}")
        conn.close()
    except WindowsError:
        print(f"[ERROR] {addr} client crash")
        del CONN_LIST[CONN_LIST.index(conn)]
        del CONNECTED_LIST[CONNECTED_LIST.index(addr)]


def to_client(conn):
    while True:
        msg = input()
        conn.send(msg.encode(FORMAT))


# функция запуска сервера на прослушивание
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # если есть коннект клиента то он принимается. conn - объект сокет, addr -
        # адрес и порт клиента
        CONNECTED_LIST.append(addr)
        CONN_LIST.append(conn)
        thread = threading.Thread(target=handle_client,
                                  args=(conn, addr))  # запуст треда на функцию handle
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        to_client(conn)


start()