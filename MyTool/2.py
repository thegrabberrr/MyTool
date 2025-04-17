import sys
import requests
import concurrent.futures
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QPalette, QBrush, QPixmap
from PySide6.QtCore import Qt


class DiscordMessenger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord send message token")
        self.setFixedSize(600, 500)

        self.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #5865F2;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
        """)

        self.set_background("background.jpg")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setText('<span style="font-size:40pt; font-weight:bold; color:white;">𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝘾𝙏𝙍𝙇-𝙓</span>')
        self.welcome_label.setMaximumHeight(100)
        layout.addWidget(self.welcome_label)

        self.token_label = QLabel("Discord Token:")
        layout.addWidget(self.token_label)

        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.token_input)

        self.message_label = QLabel("Message to send:")
        layout.addWidget(self.message_label)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(50)
        layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message_to_friends)
        layout.addWidget(self.send_button)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    def set_background(self, image_path):
        bg = QPixmap(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(bg.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def log(self, message):
        self.log_box.append(message)

    def send_message_to_friends(self):
        token = self.token_input.text().strip()
        message = self.message_input.toPlainText().strip()

        if not token or not message:
            QMessageBox.warning(self, "Missing Fields", "Please enter your token and message.")
            return

        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=self.headers)
            response.raise_for_status()
            self.friends = [user for user in response.json() if user["type"] == 1]
            self.log(f"🟢 Found {len(self.friends)} friends.\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch friends: {e}")
            return

        def send_dm(friend):
            try:
                dm_payload = {"recipient_id": friend["id"]}
                dm = requests.post("https://discord.com/api/v9/users/@me/channels", headers=self.headers, json=dm_payload)
                if dm.status_code == 200:
                    channel_id = dm.json()["id"]
                    msg_payload = {"content": message}
                    send = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=self.headers, json=msg_payload)
                    if send.status_code == 200:
                        self.log(f"✅ Message sent to: {friend['user']['username']}")
                    else:
                        self.log(f"❌ Failed to send to: {friend['user']['username']} (status {send.status_code})")
                else:
                    self.log(f"❌ Couldn't create DM channel with: {friend['user']['username']} (status {dm.status_code})")
            except Exception as e:
                self.log(f"⚠️ Error with {friend['user']['username']}: {e}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(send_dm, self.friends)

        QMessageBox.information(self, "Done", "Messages sent.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordMessenger()
    window.show()
    sys.exit(app.exec())
