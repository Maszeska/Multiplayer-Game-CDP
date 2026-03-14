import socket
import pickle
import threading


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server = "192.168.68.59"
        self.port = 5555
        self.addr = (self.server, self.port)

        self.start_pos = self.connect()

        self.all_players_data = [None, None, None, None]
        self.running = True

        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            return None

    def _receive_loop(self):
        while self.running:
            try:
                raw_data = self.client.recv(4096)
                if raw_data:
                    self.all_players_data = pickle.loads(raw_data)
            except:
                break

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
        except Exception as e:
            print("Błąd wysyłania:", e)

        return self.all_players_data