import socket
import threading
import pickle

server = "0.0.0.0" # Pre LAN hru tu napíšte "0.0.0.0"
port = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server spustený a čaká na pripojenie 2 hráčov...")

# Základný stav hry od ktorého začíname
game_state = {
    0: {"x": 150, "y": 425, "anim": 0, "na_zemi": True}, # Dátový paket Hráča 1
    1: {"x": 650, "y": 425, "anim": 0, "na_zemi": True}, # Dátový paket Hráča 2
    "ball": {"x": 200, "y": 425, "vel_x": 0, "vel_y": 0, "waiting": True},
    "score": [0, 0],
    "game_over": False,
    "players_connected": 0,
    "start_game": False
}

players_connected = 0
connections = [None, None]

def threaded_client(conn, player):
    global players_connected
    conn.send(pickle.dumps(player))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if not data:
                print("Klient bol odpojený")
                break
            else:
                # Update statusu na serveri na základe toho, čo poslal klient
                if "hrac" in data:
                    game_state[player] = data["hrac"]
                if "start_game" in data and data["start_game"]:
                    game_state["start_game"] = True
                if "reset_start" in data and data["reset_start"]:
                    game_state["start_game"] = False
                
                # Klient 0 (Yamal) spravuje všetku logiku pre loptičku
                if player == 0:
                    if "ball" in data:
                        game_state["ball"] = data["ball"]
                    if "score" in data:
                        game_state["score"] = data["score"]
                    if "game_over" in data:
                        game_state["game_over"] = data["game_over"]

                # Klientovi sa pošle naspäť celkový stav siete
                reply = game_state
                conn.sendall(pickle.dumps(reply))
        except:
            break
            
    players_connected -= 1
    game_state["players_connected"] = players_connected
    game_state["ball"]["waiting"] = True
    game_state["start_game"] = False
    connections[player] = None
    print(f"Spojenie stratené s hráčom {player}")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Prepojné k:", addr)
    if players_connected < 2:
        player = players_connected
        connections[player] = conn
        threading.Thread(target=threaded_client, args=(conn, player)).start()
        players_connected += 1
        game_state["players_connected"] = players_connected
        if players_connected == 2:
            game_state["ball"]["waiting"] = False
