import socket, threading, sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (socket.gethostbyname(socket.gethostname()), 12345)

server.bind(ADDR)
server.listen()
print("Server is listening ...")

client_server, client_addr = server.accept()
print(f"{client_addr} is connected !")

client_server.send("You are connected!".encode("utf-8"))

stop_event = threading.Event()

def send_msg():
    while not stop_event.is_set():
        try:
            msg = "YOU: "
            client_server.send(msg.encode('utf-8'))

            if msg == "quit":
                stop_event.set()
                try:
                    client_server.shutdown(socket.SHUT_RDWR)
                except:
                    pass

        except:
            break

def recv_msg():
    while not stop_event:
        try:
            msg = client_server.recv(1024).decode('utf-8')

        except:
            break

send_msg_thread = threading.Thread(target=send_msg)
recv_msg_thread = threading.Thread(target=recv_msg)

send_msg_thread.start()
recv_msg_thread.start()

send_msg_thread.join()
recv_msg_thread.join()

client_server.close()