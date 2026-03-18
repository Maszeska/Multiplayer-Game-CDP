import pickle
import socket
import time
from settings import *

server = SERVER_IP
port = SERVER_PORT

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
    state_changed = False  # Flaga sprawdzająca, czy serwer musi zaktualizować graczy

    # 1. SPRAWDZANIE TIMEOUTÓW
    for pid in list(player_last_seen.keys()):
        if current_time - player_last_seen[pid] > TIMEOUT_LIMIT:
            print(f"Gracz {pid} stracił połączenie. Usuwam z serwera.")
            players[pid] = None
            del player_addrs[pid]
            del player_last_seen[pid]
            state_changed = True

    # 2. ODBIERANIE DANYCH
    try:
        raw_data, addr = s.recvfrom(4096)
        data = pickle.loads(raw_data)

        if data == "join":
            player_id = get_free_id()
            if player_id is not None:
                player_addrs[player_id] = addr
                player_last_seen[player_id] = current_time
                s.sendto(pickle.dumps(player_id), addr)
                print(f"Gracz {player_id} dołączył z {addr}")
            else:
                s.sendto(pickle.dumps("Server is full!"), addr)
            # Pomijamy broadcast, by gracz najpierw odebrał swoje ID a nie mapę!
            continue

        elif data == "quit":
            for pid, p_addr in list(player_addrs.items()):
                if p_addr == addr:
                    print(f"Gracz {pid} wyszedł z gry. Usuwam.")
                    players[pid] = None
                    del player_addrs[pid]
                    del player_last_seen[pid]
                    state_changed = True
                    break

        elif data == "ping":
            for pid, p_addr in list(player_addrs.items()):
                if p_addr == addr:
                    player_last_seen[pid] = current_time
                    state_changed = True
                    break

        elif isinstance(data, tuple) and len(data) == 2:
            player_id, player_data = data
            if player_id in player_addrs and addr == player_addrs[player_id]:
                players[player_id] = player_data
                player_last_seen[player_id] = current_time
                state_changed = True

    except socket.timeout:
        pass
    except Exception as e:
        pass # Ignorujemy niechciane pakiety

    # 3. BROADCAST MAPY (Rozsyłamy do wszystkich naraz)
        # 3. BROADCAST MAPY (Rozsyłamy do wszystkich naraz)
    if state_changed:
        encoded_players = pickle.dumps(players)

        # NOWE: Pakujemy oficjalną liczbę połączonych graczy
        encoded_count = pickle.dumps(f"COUNT:{len(player_addrs)}")

        for pid, p_addr in list(player_addrs.items()):
            try:
                s.sendto(encoded_players, p_addr)
                s.sendto(encoded_count, p_addr)  # Wysyłamy licznik w ślad za mapą
            except:
                pass