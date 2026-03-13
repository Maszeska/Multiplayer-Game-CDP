import json
import socket
import threading

import pygame

from board import Board
from bomb import Bomb
from player import Player
from settings import *
from menu import MainMenu
from options_menu import OptionsMenu


class NetworkPeer:
    def __init__(self, mode, host="127.0.0.1", port=5555):
        self.mode = mode  # "server" or "client"
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.recv_thread = None
        self.running = False

        self.remote_state = {"x": 0, "y": 0}
        self.remote_bombs = []
        self.connected = False

    def start(self):
        self.running = True
        if self.mode == "server":
            threading.Thread(target=self._start_server, daemon=True).start()
        else:
            threading.Thread(target=self._start_client, daemon=True).start()

    def stop(self):
        self.running = False
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
        try:
            if self.sock:
                self.sock.close()
        except:
            pass

    def _start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))  # Listen on all interfaces (VPN/LAN)
        self.sock.listen(1)

        print(f"[net] server listening on {self.host}:{self.port}")
        self.conn, _ = self.sock.accept()
        print("[net] client connected")
        self.connected = True
        self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self.recv_thread.start()

    def _start_client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.conn = self.sock
            self.connected = True
            print(f"[net] connected to server {self.host}:{self.port}")
            self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
            self.recv_thread.start()
        except Exception as e:
            print("[net] connection failed:", e)

    def _recv_loop(self):
        buf = b""
        while self.running and self.conn:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line:
                        continue
                    try:
                        msg = json.loads(line.decode("utf-8"))
                    except Exception:
                        continue
                    self._handle_msg(msg)
            except Exception:
                break

    def _handle_msg(self, msg):
        t = msg.get("type")
        if t == "state":
            self.remote_state["x"] = msg.get("x", 0)
            self.remote_state["y"] = msg.get("y", 0)
        elif t == "bomb":
            self.remote_bombs.append((msg.get("x", 0), msg.get("y", 0)))

    def send(self, msg):
        if not self.connected:
            return
        try:
            payload = (json.dumps(msg) + "\n").encode("utf-8")
            self.conn.sendall(payload)
        except Exception:
            pass


def connection_screen(screen, font):
    """Return (mode, host, port) once user confirms."""
    input_text = ""
    port_text = "5555"
    mode = None  # "server" or "client"
    prompt = "H: host  J: join"
    info = "Enter server IP (for join) or leave blank for localhost."

    clock = pygame.time.Clock()
    while True:
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    mode = "server"
                elif event.key == pygame.K_j:
                    mode = "client"
                elif event.key == pygame.K_RETURN and mode:
                    return mode, input_text.strip() or "127.0.0.1", int(port_text)
                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        port_text = port_text[:-1]
                    else:
                        input_text = input_text[:-1]
                else:
                    if event.unicode.isdigit() and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # if shift pressed treat input as port
                        port_text += event.unicode
                    elif event.unicode in "0123456789." and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # allow typing IP with dots
                        input_text += event.unicode
                    elif event.unicode.isalpha() and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        input_text += event.unicode

        y = 200
        for line in [prompt, info, f"IP: {input_text}", f"PORT: {port_text}", f"MODE: {mode or 'none'}", "ENTER to confirm"]:
            surf = font.render(line, True, "white")
            screen.blit(surf, (50, y))
            y += 50

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boomit! (networked)")

    try:
        game_icon = pygame.image.load(ICON_PATH).convert_alpha()
        pygame.display.set_icon(game_icon)
    except pygame.error:
        print("Nie udało się załadować ikonki okna.")

    timer = pygame.time.Clock()

    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Nie znaleziono pliku muzycznego, gra uruchomi się bez dźwięku.")

    game_board = Board(BOARD)

    start_x = game_board.offset_x + game_board.tile_size
    start_y = game_board.offset_y + game_board.tile_size
    player = Player(start_x, start_y, game_board.tile_size)

    remote_player = Player(start_x, start_y, game_board.tile_size)

    main_menu = MainMenu()
    options_menu = OptionsMenu()

    # new connection step
    font = pygame.font.SysFont(MENU_FONT_PATH, 30, bold=True)
    mode, host, port = connection_screen(screen, font)
    if not mode:
        pygame.quit()
        return

    net = NetworkPeer(mode, host, port)
    net.start()

    # New waiting screen
    waiting = True
    font = pygame.font.SysFont(MENU_FONT_PATH, 50, bold=True)
    while waiting:
        screen.fill("black")

        if net.connected:
            text = "Connected! Press ENTER to start game"
        else:
            text = "Waiting for connection..."

        surf = font.render(text, True, "white")
        screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                net.stop()
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and net.connected:
                waiting = False

        timer.tick(FPS)  # Prevent high CPU usage

    game_state = "shaking"  # Skip menu, go directly to game
    active_bombs = []
    remote_bombs = []

    running = True
    while running:
        timer.tick(FPS)
        is_moving = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "menu":
                clicked_button = main_menu.handle_event(event)
                if clicked_button == "PLAY":
                    game_state = "shaking"
                elif clicked_button == "OPTIONS":
                    game_state = "options"
            elif game_state == "options":
                clicked_button = options_menu.handle_event(event)
                if clicked_button == "BACK":
                    game_state = "menu"

            if event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_SPACE and len(active_bombs) < 2:
                        new_bomb = player.drop_bomb(game_board)
                        active_bombs.append(new_bomb)
                        net.send({"type": "bomb", "x": new_bomb.x, "y": new_bomb.y})

        if game_state == "playing":
            # Server uses WASD, client uses arrows
            use_arrows = (mode == "client")
            is_moving = player.move(game_board, use_arrows=use_arrows)

            # Always send local position updates to the peer (even if not moving)
            net.send({"type": "state", "x": player.x, "y": player.y})

        if game_state == "menu":
            main_menu.draw(screen)

        elif game_state == "options":
            options_menu.draw(screen)

        else:
            game_board.draw(screen)

            remote_player.x = net.remote_state["x"]
            remote_player.y = net.remote_state["y"]

            for bomb in active_bombs:
                bomb.update(game_board)
                bomb.draw(screen, game_board)

            while net.remote_bombs:
                bx, by = net.remote_bombs.pop(0)
                remote_bombs.append(Bomb(bx, by, game_board.tile_size))

            for bomb in remote_bombs:
                bomb.update(game_board)
                bomb.draw(screen, game_board)
            remote_bombs = [b for b in remote_bombs if b.state != "done"]

            active_bombs = [bomb for bomb in active_bombs if bomb.state != "done"]

            if game_state == "shaking":
                if player.shake_timer >= SHAKE_DURATION:
                    game_state = "hatching"
            elif game_state == "hatching":
                if int(player.hatch_frame_index) >= len(player.hatch_frames):
                    game_state = "playing"

            player.draw(screen, game_state, is_moving)
            remote_player.draw(screen, game_state, False)

        pygame.display.flip()

    net.stop()
    pygame.quit()


if __name__ == "__main__":
    main()