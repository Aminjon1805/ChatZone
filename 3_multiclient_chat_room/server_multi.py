import selectors
import socket

HOST = '127.0.0.1'
PORT = 12345

sel = selectors.DefaultSelector()

def accept(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn):
    try:
        data = conn.recv(1024)
        if data:
            broadcast(conn, data)
        else:
            close_connection(conn)
    except:
        close_connection(conn)

def broadcast(sender_conn, message):
    for key in sel.get_map().values():
        if key.fileobj not in (server_socket, sender_conn):
            try:
                key.fileobj.send(message)
            except:
                close_connection(key.fileobj)

def close_connection(conn):
    print(f"Closing connection {conn}")
    sel.unregister(conn)
    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
server_socket.setblocking(False)

sel.register(server_socket, selectors.EVENT_READ, accept)

print(f"Server running on {HOST}:{PORT}")

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sel.close()
