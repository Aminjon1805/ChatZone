import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("Server closed connection.")
                break
            print(message.decode('utf-8'))
        except:
            print("Error receiving message.")
            break

def send_messages():
    while True:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
        except:
            print("Error sending message.")
            break

recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

send_messages()

client_socket.close()
