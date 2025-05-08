import sys, socket, threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class ChatClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatZone - Client")
        self.setGeometry(600, 300, 400, 400)

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

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())  # or enter IP of server
        self.client.connect((host, 12345))
        welcome = self.client.recv(1024).decode("utf-8")
        self.chat_display.append(f"Server: {welcome}")

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
                    self.chat_display.append("Server disconnected.")
                    self.stop_event.set()
                    self.client.close()
                    break
                self.chat_display.append(f"Server: {msg}")
            except:
                break

    def closeEvent(self, event):
        self.stop_event.set()
        try:
            self.client.close()
        except:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatClientApp()
    window.show()
    sys.exit(app.exec())
