import os
import sys
import requests
from io import BytesIO

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QMenu
)
from PySide6.QtGui import QPixmap, QImage, QAction, QTextCursor
from PySide6.QtCore import Qt

# Global variables
selected_folder = None
found_files = []
original_lines = {}

def identify_service(email):
    if "@netflix.com" in email.lower():
        return "Netflix"
    elif "@shein.com" in email.lower():
        return "Shein"
    else:
        return None

def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = QImage.fromData(response.content)
        image = image.scaled(950, 700, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        return QPixmap.fromImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return QPixmap()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BytesShadow")
        self.setFixedSize(950, 700)

        self.pixmap_background = load_image_from_url("https://image.noelshack.com/fichiers/2025/15/2/1744079295-wp2678303.png")
        self.label_background = QLabel(self)
        self.label_background.setPixmap(self.pixmap_background)
        self.label_background.setGeometry(0, 0, 950, 700)
        self.label_background.setScaledContents(True)
        self.label_background.lower()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(150, 2, 150, 2)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.label_instruction = QLabel("𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓽𝓸 𝓽𝓱𝓮 𝓑𝔂𝓽𝓮𝓢𝓱𝓪𝓭𝓸𝔀 𝓹𝓪𝓷𝓮𝓵 ツ", self)
        self.label_instruction.setStyleSheet("color: white; font: 20pt 'Arial'; background-color: rgba(0, 0, 0, 150);")
        self.label_instruction.setFixedHeight(35)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_instruction)
        
        self.label_instruction = QLabel("𝐒𝐞𝐚𝐫𝐜𝐡 𝐟𝐨𝐫 𝐝𝐚𝐭𝐚...", self)
        self.label_instruction.setStyleSheet("color: white; font: 12pt 'Arial'; background-color: rgba(0, 0, 0, 150);")
        self.label_instruction.setFixedHeight(25)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_instruction)

        self.label_instruction = QLabel("𝐁𝐫𝐨𝐰𝐬𝐞 𝐚 𝐟𝐨𝐥𝐝𝐞𝐫 𝐰𝐢𝐭𝐡 .𝐭𝐱𝐭 𝐟𝐢𝐥𝐞𝐬", self)
        self.label_instruction.setStyleSheet("color: white; font: 10pt 'Arial'; background-color: rgba(0, 0, 0, 150);")
        self.label_instruction.setFixedHeight(25)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_instruction)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(2)

        self.button_folder = QPushButton("📂 𝐁𝐫𝐨𝐰𝐬𝐞", self)
        self.button_folder.setStyleSheet("color: white; background-color: rgba(50,50,50,150);")
        self.button_folder.setFixedHeight(30)
        self.button_folder.clicked.connect(self.choose_folder)
        self.button_layout.addWidget(self.button_folder)

        # 👉 Nouveau bouton Clear ici
        self.button_clear = QPushButton("🧹 𝐂𝐥𝐞𝐚𝐫", self)
        self.button_clear.setStyleSheet("color: white; background-color: rgba(50,50,50,150);")
        self.button_clear.setFixedHeight(30)
        self.button_clear.clicked.connect(self.clear_results)
        self.button_layout.addWidget(self.button_clear)

        self.button_search = QPushButton("𝐒𝐞𝐚𝐫𝐜𝐡", self)
        self.button_search.setStyleSheet("color: white; background-color: rgba(50,50,50,150);")
        self.button_search.setFixedHeight(30)
        self.button_search.clicked.connect(self.search_username_interface)
        self.button_layout.addWidget(self.button_search)

        self.layout.addLayout(self.button_layout)

        self.label_folder = QLabel("𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐟𝐨𝐥𝐝𝐞𝐫 : 𝐍𝐨𝐧𝐞", self)
        self.label_folder.setStyleSheet("color: white; font: 10pt 'Arial'; background-color: rgba(0,0,0,150);")
        self.label_folder.setFixedHeight(20)
        self.label_folder.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_folder)

        self.entry_username = QLineEdit(self)
        self.entry_username.setStyleSheet("color: white; font: 12pt 'Arial'; background-color: rgba(50,50,50,150);")
        self.entry_username.setFixedHeight(30)
        self.entry_username.returnPressed.connect(self.search_username_interface)
        self.layout.addWidget(self.entry_username)

        self.results = QTextEdit(self)
        self.results.setReadOnly(True)
        self.results.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0);"
            "color: white;"
            "font-family: Courier;"
            "border: none;"
        )
        self.results.setFixedHeight(300)
        self.layout.addWidget(self.results)

        self.results.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results.customContextMenuRequested.connect(self.show_right_click_menu)

    def choose_folder(self):
        global selected_folder
        folder = QFileDialog.getExistingDirectory(self, "Choose the folder with .txt files")
        if folder:
            selected_folder = folder
            self.label_folder.setText(f"𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐟𝐨𝐥𝐝𝐞𝐫 : {selected_folder}")

    def search_username_interface(self):
        global found_files, original_lines, selected_folder

        username = self.entry_username.text().strip()
        found_files.clear()
        original_lines.clear()

        if not selected_folder or not username:
            return

        self.results.setPlainText("")
        found = False

        for file_name in os.listdir(selected_folder):
            file_path = os.path.join(selected_folder, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".txt"):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        lines = file.readlines()
                        original_lines[file_path] = lines[:]

                        for i, line in enumerate(lines):
                            if username in line:
                                found = True
                                line = line.strip()
                                words = line.split()
                                service = None
                                for word in words:
                                    if "@" in word:
                                        service = identify_service(word)
                                        break

                                if service:
                                    self.results.append(f"✅ {service:<12}:{file_name:<20}: {line}")
                                else:
                                    self.results.append(f"✅ Found: {file_name:<20}: {line}")
                                found_files.append((file_path, i, line))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        if not found:
            self.results.append("No results found")

        self.results.moveCursor(QTextCursor.Start)

    def clear_results(self):
        self.results.clear()
        self.entry_username.clear()

    def show_right_click_menu(self, point):
        menu = QMenu(self)
        action_copy = QAction("📋 Copy", self)
        action_copy.triggered.connect(self.copy_selected_text)
        menu.addAction(action_copy)
        menu.exec(self.results.mapToGlobal(point))

    def copy_selected_text(self):
        selection = self.results.textCursor().selectedText()
        if selection.strip():
            clipboard = QApplication.clipboard()
            clipboard.setText(selection)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
