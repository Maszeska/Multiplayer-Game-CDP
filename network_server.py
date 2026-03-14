import pickle
import socket
import threading

server = "192.168.68.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(4)
print("Serwer started. Waiting for connections...")

player_count = 0
players = [None, None, None, None]

def threaded_client(conn, player_id):
    global players

    conn.send(str.encode(str(player_id)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print(f"Player {player_id} disconnected.")
                break

            players[player_id] = data
            conn.sendall(pickle.dumps(players))

        except socket.error:
            print(f"Lost connection with Player {player_id}")
            break

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