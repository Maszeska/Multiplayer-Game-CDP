import pickle
import socket
import time

server = "100.83.138.125"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

print("UDP Server started. Waiting for connections...")

player_count = 0
players = [None, None, None, None]
player_addrs = {}  # Map player_id to client address

while True:
    try:
        raw_data, addr = s.recvfrom(4096)
        data = pickle.loads(raw_data)

        if data == "join":
            if player_count < 4:
                player_id = player_count
                player_count += 1
                player_addrs[player_id] = addr
                s.sendto(pickle.dumps(player_id), addr)
                print(f"Player {player_id} joined from {addr}")
            else:
                s.sendto(pickle.dumps("Server is full!"), addr)
                print(f"Server full. Denied connection from {addr}")
        else:
            player_id, player_data = data
            if player_id in player_addrs and addr == player_addrs[player_id]:
                players[player_id] = player_data
                # Send updated players list to all connected clients
                for client_addr in player_addrs.values():
                    s.sendto(pickle.dumps(players), client_addr)
            else:
                print(f"Invalid data from {addr}, player_id {player_id}")

    except Exception as e:
        print(f"Server error: {e}")

    time.sleep(0.001)