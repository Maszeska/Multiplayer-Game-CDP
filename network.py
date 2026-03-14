import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server = "26.219.166.236"
        self.port = 5555
        self.addr = (self.server, self.port)

        self.start_pos = self.connect()
        print("Otrzymane ID od serwera:", self.start_pos)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print("Błąd połączenia:", e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)