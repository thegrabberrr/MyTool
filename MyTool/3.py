import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor

class WebhookSender(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Webhook Sender")
        self.setFixedSize(480, 300)

        # Webhook URL
        self.label_webhook = QLabel("Webhook URL:")
        self.input_webhook = QLineEdit()

        # Message
        self.label_message = QLabel("Message:")
        self.input_message = QTextEdit()
        self.input_message.setFixedHeight(60)

        # Message count
        self.label_count = QLabel("Number of messages:")
        self.input_count = QSpinBox()
        self.input_count.setRange(1, 1000)
        self.input_count.setValue(10)

        # Buttons
        self.button_send = QPushButton("Send")
        self.button_spam = QPushButton("Spam")

        # Status label
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label_webhook)
        layout.addWidget(self.input_webhook)
        layout.addWidget(self.label_message)
        layout.addWidget(self.input_message)
        layout.addWidget(self.label_count)
        layout.addWidget(self.input_count)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_send)
        buttons_layout.addWidget(self.button_spam)
        layout.addLayout(buttons_layout)

        layout.addWidget(self.status)
        self.setLayout(layout)

        # Connect buttons
        self.button_send.clicked.connect(self.send_message)
        self.button_spam.clicked.connect(self.spam_messages)

        # Apply dark mode
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor("#2f3136"))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor("#202225"))
        dark_palette.setColor(QPalette.AlternateBase, QColor("#2f3136"))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor("#7289da"))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Highlight, QColor("#5865F2"))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        self.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                padding: 6px;
                border-radius: 6px;
                background-color: #7289da;
                color: white;
            }
            QPushButton:hover {
                background-color: #5b6eae;
            }
            QLineEdit, QTextEdit, QSpinBox {
                background-color: #202225;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }
        """)

    def send_message(self):
        webhook_url = self.input_webhook.text().strip()
        message_content = self.input_message.toPlainText().strip()

        if not webhook_url or not message_content:
            self.status.setText("❌ Please enter both a webhook URL and a message.")
            return

        self.toggle_inputs(False)
        message = {"content": message_content}

        try:
            response = requests.post(webhook_url, json=message)
            if response.status_code in [200, 204]:
                self.status.setText("✅ Message sent successfully.")
            else:
                self.status.setText(f"❌ Error {response.status_code}")
        except Exception as e:
            self.status.setText(f"❌ Exception: {e}")

        QTimer.singleShot(1000, lambda: self.toggle_inputs(True))

    def spam_messages(self):
        webhook_url = self.input_webhook.text().strip()
        message_content = self.input_message.toPlainText().strip()
        count = self.input_count.value()

        if not webhook_url or not message_content:
            self.status.setText("❌ Please enter both a webhook URL and a message.")
            return

        self.toggle_inputs(False)
        self.status.setText("📤 Sending messages...")
        message = {"content": message_content}

        success = 0
        for _ in range(count):
            try:
                response = requests.post(webhook_url, json=message)
                if response.status_code in [200, 204]:
                    success += 1
            except Exception:
                continue

        self.status.setText(f"✅ {success}/{count} messages sent.")
        QTimer.singleShot(1000, lambda: self.toggle_inputs(True))

    def toggle_inputs(self, enabled: bool):
        self.button_send.setEnabled(enabled)
        self.button_spam.setEnabled(enabled)
        self.input_webhook.setEnabled(enabled)
        self.input_message.setEnabled(enabled)
        self.input_count.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebhookSender()
    window.show()
    sys.exit(app.exec())
