import socket
import threading
import datetime

class Client:
    def __init__(self, nickname, conn, addr, channel):
        self.nickname = nickname
        self.conn = conn
        self.addr = addr
        self.channel = channel

def handle_client(client):
    while True:
        try:
            message = client.conn.recv(1024).decode('utf-8')
            broadcast(message, client)
        except:
            remove_client(client)
            break

def broadcast(message, sender_client):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {sender_client.nickname}: {message}"
    for client in clients:
        if client != sender_client and client.channel == sender_client.channel:
            client.conn.send(formatted_message.encode('utf-8'))

def remove_client(client):
    clients.remove(client)
    client.conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

clients = []

while True:
    conn, addr = server.accept()
    nickname = conn.recv(1024).decode('utf-8')
    channel = conn.recv(1024).decode('utf-8')
    new_client = Client(nickname, conn, addr, channel)
    clients.append(new_client)

    print(f"{nickname} connected to {channel}")
    threading.Thread(target=handle_client, args=(new_client,)).start()
