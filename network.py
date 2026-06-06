import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.9" # Zmeňte na IP v LAN, ak hráte na 2 PC (napr. "192.168.1.5")
        self.port = 8001
        self.addr = (self.server, self.port)
        self.p = self.connect() # id hraca (0 alebo 1)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("Chyba pri pripájaní na server:", e)
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Chyba odosielania:", e)