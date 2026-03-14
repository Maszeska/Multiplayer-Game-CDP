import socket
import pickle
import threading


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "100.83.138.125"
        self.port = 5555
        self.server_addr = (self.server, self.port)

        # Bind to a random available port for receiving
        self.client.bind(('', 0))
        self.local_addr = self.client.getsockname()

        self.start_pos = self.join()

        self.all_players_data = [None, None, None, None]
        self.running = True

        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()

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

    def _receive_loop(self):
        while self.running:
            try:
                raw_data, addr = self.client.recvfrom(4096)
                if addr == self.server_addr:
                    self.all_players_data = pickle.loads(raw_data)
            except:
                break

    def send(self, data):
        try:
            packet = pickle.dumps((self.start_pos, data))
            self.client.sendto(packet, self.server_addr)
        except Exception as e:
            print("Send error:", e)

        return self.all_players_data