import socket
import threading

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection lost")
            break

def send_messages():
    while True:
        message = input()
        client.send(message.encode('utf-8'))

server_ip = input("Enter server IP: ")
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 5555))
client.send(nickname.encode('utf-8'))

channel = input("Enter a channel name: ")
client.send(channel.encode('utf-8'))

print("Connected to the server")

threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()
