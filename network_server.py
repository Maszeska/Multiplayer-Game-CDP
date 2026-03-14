import pickle
import socket
import threading
import time

server = "192.168.68.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(4)
print("Server started. Waiting for connections...")

player_count = 0
players = [None, None, None, None]

def threaded_client(conn, player_id):
    global players
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    conn.send(str.encode(str(player_id)))

    while True:
        try:
            raw_data = conn.recv(4096)
            if not raw_data:
                break

            data = pickle.loads(raw_data)
            players[player_id] = data
            conn.sendall(pickle.dumps(players))

        except Exception as e:
            print(f"Błąd gracza {player_id}: {e}")
            break

    print(f"Gracz {player_id} rozłączony.")
    players[player_id] = None
    conn.close()

while True:
    conn, addr = s.accept()
    print("New player connected:", addr)
    if player_count < 4:
        threading.Thread(target=threaded_client, args=(conn, player_count)).start()
        player_count += 1
    else:
        print("Server is full. Connection denied for:", addr)
        conn.send(str.encode("Server is full!"))
        conn.close()
    time.sleep(0.001)