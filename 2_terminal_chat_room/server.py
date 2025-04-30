# ONE VS ONE TERMINAL CHAT ROOM! (Server Part)

import socket
import threading
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 12345))
server.listen()
print("Server is listening...")

client, addr = server.accept()
print(f"Client {addr} connected.")
client.send("You are connected!".encode("utf-8"))

stop_event = threading.Event()

def send_msg():
    while not stop_event.is_set():
        try:
            msg = input("YOU: ")
            client.send(msg.encode("utf-8"))
            if msg == "quit":
                stop_event.set()
                try:
                    client.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                client.close()
                break
        except:
            break

def receive_msg():
    while not stop_event.is_set():
        try:
            msg = client.recv(1024).decode("utf-8")
            if not msg or msg == "quit":
                print("Client disconnected.")
                stop_event.set()
                try:
                    client.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                client.close()
                break
            sys.stdout.write(f"\rCLIENT: {msg}\nYOU: ")
            sys.stdout.flush()
        except:
            break

thread_send = threading.Thread(target=send_msg)
thread_receive = threading.Thread(target=receive_msg)

thread_receive.start()
thread_send.start()

thread_send.join()
thread_receive.join()

server.close()
