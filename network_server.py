import pickle
import socket
import time
from settings import *

#----------------------------------------------------
# Game Server
#----------------------------------------------------

server = SERVER_IP
port = SERVER_PORT

                                        # --- UDP ---
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server, port))
s.settimeout(0.5)

print("UDP Server started. Waiting for connections...")

players = [None, None, None, None]
player_addrs = {}
player_last_seen = {}

TIMEOUT_LIMIT = 3.0


def get_free_id():
    for i in range(4):
        if i not in player_addrs:
            return i
    return None


while True:
    current_time = time.time()
    state_changed = False

    # Handle: disconnect player if not seen in {TIMEOUT_LIMIT} seconds
    for pid in list(player_last_seen.keys()):
        if current_time - player_last_seen[pid] > TIMEOUT_LIMIT:
            print(f"Player {pid} lost connection. Deleting from server...")
            players[pid] = None
            del player_addrs[pid]
            del player_last_seen[pid]
            state_changed = True


    # Handle: Receive data
    try:
        # catch data
        raw_data, addr = s.recvfrom(4096)
        data = pickle.loads(raw_data)

        # Case: player wants to join server
        if data == "join":
            player_id = get_free_id()
            if player_id is not None:
                player_addrs[player_id] = addr
                player_last_seen[player_id] = current_time
                s.sendto(pickle.dumps(player_id), addr)
                print(f"Gracz {player_id} dołączył z {addr}")
            else:
                s.sendto(pickle.dumps("Server is full!"), addr)
            continue

        # Case: player intentionally left the server
        elif data == "quit":
            for pid, p_addr in list(player_addrs.items()):
                if p_addr == addr:
                    print(f"Player {pid} Left game. Deleting from server...")
                    players[pid] = None
                    del player_addrs[pid]
                    del player_last_seen[pid]
                    state_changed = True
                    break

        # Case: player pings to reset the stop-watch
        elif data == "ping":
            for pid, p_addr in list(player_addrs.items()):
                if p_addr == addr:
                    player_last_seen[pid] = current_time
                    state_changed = True
                    break

        # Tuple of player X data
        elif isinstance(data, tuple) and len(data) == 2:
            player_id, player_data = data
            if player_id in player_addrs and addr == player_addrs[player_id]:
                players[player_id] = player_data
                player_last_seen[player_id] = current_time
                state_changed = True

    except socket.timeout:
        pass
    except Exception as e:
        pass # Ignore unwanted packets


    # Handle: Update everyone on Change
    if state_changed:
        # pack players data
        encoded_players = pickle.dumps(players)

        # pack data on N of players
        encoded_count = pickle.dumps(f"COUNT:{len(player_addrs)}")

        # Send package to every player
        for pid, p_addr in list(player_addrs.items()):
            try:
                s.sendto(encoded_players, p_addr)
                s.sendto(encoded_count, p_addr)
            except:
                pass