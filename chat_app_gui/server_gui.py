import sys, socket, threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class ChatServerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatZone - Server")
        self.setGeometry(500, 300, 400, 400)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.input_field = QLineEdit(self)
        self.send_button = QPushButton("Send", self)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

        self.stop_event = threading.Event()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        self.server.bind((host, 12345))
        self.server.listen()
        self.chat_display.append(f"Server started at {host}:12345\nWaiting for client...")

        threading.Thread(target=self.accept_client, daemon=True).start()

    def accept_client(self):
        self.client, addr = self.server.accept()
        self.chat_display.append(f"Client {addr} connected.")
        self.client.send("You are connected!".encode("utf-8"))
        threading.Thread(target=self.receive_message, daemon=True).start()

    def send_message(self):
        msg = self.input_field.text()
        if msg:
            self.chat_display.append(f"You: {msg}")
            try:
                self.client.send(msg.encode("utf-8"))
            except:
                self.chat_display.append("Failed to send message.")
            if msg == "quit":
                self.stop_event.set()
                self.client.close()
            self.input_field.clear()

    def receive_message(self):
        while not self.stop_event.is_set():
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if not msg or msg == "quit":
                    self.chat_display.append("Client disconnected.")
                    self.stop_event.set()
                    self.client.close()
                    break
                self.chat_display.append(f"Client: {msg}")
            except:
                break

    def closeEvent(self, event):
        self.stop_event.set()
        try:
            self.client.close()
        except:
            pass
        self.server.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatServerApp()
    window.show()
    sys.exit(app.exec())
