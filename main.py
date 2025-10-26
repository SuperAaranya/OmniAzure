from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QFileDialog, QInputDialog
from PySide6.QtCore import Qt
import os, subprocess, sys, webbrowser

class OmniAzure(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OmniAzure")
        self.setGeometry(100, 100, 600, 500)
        self.layout = QVBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type path, command, or URL")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.create_file_btn = QPushButton("Create File")
        self.create_folder_btn = QPushButton("Create Folder")
        self.delete_btn = QPushButton("Delete File/Folder")
        self.rename_btn = QPushButton("Rename File/Folder")
        self.move_btn = QPushButton("Move File/Folder")
        self.run_app_btn = QPushButton("Run App/Script")
        self.open_web_btn = QPushButton("Open Website")
        self.search_btn = QPushButton("Search File/Folder")
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.create_file_btn)
        self.layout.addWidget(self.create_folder_btn)
        self.layout.addWidget(self.delete_btn)
        self.layout.addWidget(self.rename_btn)
        self.layout.addWidget(self.move_btn)
        self.layout.addWidget(self.run_app_btn)
        self.layout.addWidget(self.open_web_btn)
        self.layout.addWidget(self.search_btn)
        self.layout.addWidget(self.output)
        self.setLayout(self.layout)
        self.create_file_btn.clicked.connect(self.create_file)
        self.create_folder_btn.clicked.connect(self.create_folder)
        self.delete_btn.clicked.connect(self.delete_item)
        self.rename_btn.clicked.connect(self.rename_item)
        self.move_btn.clicked.connect(self.move_item)
        self.run_app_btn.clicked.connect(self.run_app)
        self.open_web_btn.clicked.connect(self.open_website)
        self.search_btn.clicked.connect(self.search_item)

    def create_file(self):
        path = QFileDialog.getSaveFileName(self, "Create File")[0]
        if path:
            open(path, "w").close()
            self.output.append(f"File created: {path}")

    def create_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Parent Folder")
        if path:
            name, ok = QInputDialog.getText(self, "Folder Name", "Enter folder name:")
            if ok and name:
                full_path = os.path.join(path, name)
                os.makedirs(full_path, exist_ok=True)
                self.output.append(f"Folder created: {full_path}")

    def delete_item(self):
        path = QFileDialog.getExistingDirectory(self, "Select File/Folder") or QFileDialog.getOpenFileName(self, "Select File")[0]
        if path:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    self.output.append(f"File deleted: {path}")
                elif os.path.isdir(path):
                    os.rmdir(path)
                    self.output.append(f"Folder deleted: {path}")
            except Exception as e:
                self.output.append(f"Error: {e}")

    def rename_item(self):
        path = QFileDialog.getExistingDirectory(self, "Select File/Folder") or QFileDialog.getOpenFileName(self, "Select File")[0]
        if path:
            name, ok = QInputDialog.getText(self, "New Name", "Enter new name:")
            if ok and name:
                new_path = os.path.join(os.path.dirname(path), name)
                os.rename(path, new_path)
                self.output.append(f"Renamed to: {new_path}")

    def move_item(self):
        path = QFileDialog.getExistingDirectory(self, "Select File/Folder") or QFileDialog.getOpenFileName(self, "Select File")[0]
        if path:
            dest = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
            if dest:
                new_path = os.path.join(dest, os.path.basename(path))
                os.rename(path, new_path)
                self.output.append(f"Moved to: {new_path}")

    def run_app(self):
        path = self.input.text()
        if path:
            try:
                if sys.platform.startswith("win"):
                    os.startfile(path)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
                self.output.append(f"App/Script launched: {path}")
            except Exception as e:
                self.output.append(f"Error: {e}")

    def open_website(self):
        url = self.input.text()
        if url:
            webbrowser.open(url)
            self.output.append(f"Website opened: {url}")

    def search_item(self):
        query = self.input.text()
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Search")
        if query and folder:
            matches = []
            for root, dirs, files in os.walk(folder):
                for name in files + dirs:
                    if query.lower() in name.lower():
                        matches.append(os.path.join(root, name))
            self.output.append(f"Search results for '{query}':")
            for m in matches:
                self.output.append(m)

app = QApplication([])
window = OmniAzure()
window.show()
app.exec()