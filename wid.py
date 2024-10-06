#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox

class FileSystemGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Файловая система')
        self.setGeometry(100, 100, 600, 400)

        self.left_list = QListWidget()
        self.right_list = QListWidget()

        self.create_button = QPushButton('Создать папку')
        self.delete_button = QPushButton('Удалить')
        self.move_button = QPushButton('Переместить')

        self.create_button.clicked.connect(self.create_folder)
        self.delete_button.clicked.connect(self.delete_item)
        self.move_button.clicked.connect(self.move_item)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.move_button)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.left_list)
        folder_layout.addWidget(self.right_list)

        layout.addLayout(folder_layout)
        self.setLayout(layout)

        self.load_folders()

    def load_folders(self):
        self.left_folder = QFileDialog.getExistingDirectory(self, "Выберите левую папку")
        self.right_folder = QFileDialog.getExistingDirectory(self, "Выберите правую папку")

        self.left_list.clear()
        self.right_list.clear()

        if self.left_folder:
            for item in os.listdir(self.left_folder):
                self.left_list.addItem(item)

        if self.right_folder:
            for item in os.listdir(self.right_folder):
                self.right_list.addItem(item)

    def create_folder(self):
        current_folder = self.left_folder if self.left_list.hasFocus() else self.right_folder
        folder_name, _ = QFileDialog.getSaveFileName(self, "Введите название новой папки", current_folder)

        if folder_name:
            try:
                os.mkdir(folder_name)
                self.load_folders()
            except FileExistsError:
                QMessageBox.warning(self, "Ошибка", "Папка с таким именем уже существует.")
    
    def delete_item(self):
        current_list = self.left_list if self.left_list.hasFocus() else self.right_list
        current_folder = self.left_folder if self.left_list.hasFocus() else self.right_folder

        selected_item = current_list.currentItem()
        if selected_item:
            path_to_delete = os.path.join(current_folder, selected_item.text())
            try:
                if os.path.isdir(path_to_delete):
                    shutil.rmtree(path_to_delete)
                else:
                    os.remove(path_to_delete)
                self.load_folders()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def move_item(self):
        if self.left_list.hasFocus():
            selected_item = self.left_list.currentItem()
            src_folder = self.left_folder
            dest_folder = self.right_folder
        else:
            selected_item = self.right_list.currentItem()
            src_folder = self.right_folder
            dest_folder = self.left_folder

        if selected_item:
            src_path = os.path.join(src_folder, selected_item.text())
            dest_path = os.path.join(dest_folder, selected_item.text())
            try:
                shutil.move(src_path, dest_path)
                self.load_folders()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSystemGUI()
    window.show()
    sys.exit(app.exec_())

