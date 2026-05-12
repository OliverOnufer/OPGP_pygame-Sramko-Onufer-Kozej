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
    "game_over": False
}

def threaded_client(conn, player):
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
            
    print(f"Spojenie stratené s hráčom {player}")
    conn.close()

player_count = 0
while True:
    conn, addr = s.accept()
    print("Prepojné k:", addr)
    if player_count < 2:
        threading.Thread(target=threaded_client, args=(conn, player_count)).start()
        player_count += 1