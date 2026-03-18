import socket
import pickle
import threading
import time
from settings import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = SERVER_IP
        self.port = SERVER_PORT
        self.server_addr = (self.server, self.port)

        self.client.bind(('', 0))
        self.local_addr = self.client.getsockname()

        self.start_pos = self.join()

        self.connected_players_count = 1

        self.all_players_data = [None, None, None, None]
        self.running = True

        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()

        self.ping_thread = threading.Thread(target=self._ping_loop, daemon=True)
        self.ping_thread.start()

    def join(self):
        try:
            self.client.sendto(pickle.dumps("join"), self.server_addr)
            while True:
                data, addr = self.client.recvfrom(4096)
                if addr == self.server_addr:
                    return pickle.loads(data)
        except Exception as e:
            print("Join error:", e)
            return None

    def send(self, data):
        try:
            packet = (self.start_pos, data)
            self.client.sendto(pickle.dumps(packet), self.server_addr)

            return self.all_players_data
        except Exception as e:
            print("Send error:", e)
            return self.all_players_data

    def _receive_loop(self):
        while self.running:
            try:
                raw_data, addr = self.client.recvfrom(4096)
                if addr == self.server_addr:
                    data = pickle.loads(raw_data)

                    if isinstance(data, str) and data.startswith("COUNT:"):
                        self.connected_players_count = int(data.split(":")[1])
                    else:
                        self.all_players_data = data
            except Exception:
                pass

    def _ping_loop(self):
        while self.running:
            try:
                self.client.sendto(pickle.dumps("ping"), self.server_addr)
            except Exception:
                pass
            time.sleep(1)