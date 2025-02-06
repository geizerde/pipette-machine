import os
import sys

import serial
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QMessageBox, QRadioButton, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QWidget, QLabel

from src.app.connection import establish_connection, setup_coords
from src.app.scripts import GO, GO_HOME
from src.app.windows.edit_window import EditWindow


class MainWindow(QWidget):
    ser: serial.Serial

    window: QWidget
    connection_label: QLabel
    table: QTableWidget
    edit_button: QPushButton
    set_button: QPushButton
    move_button: QPushButton
    change_button: QPushButton
    color_buttons: QHBoxLayout

    components: []
    mode = 0
    color_buttons_count = 0
    current_color: str
    current_comp: str

    def __init__(self):
        super().__init__()
        self.components = []
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # header
        header = QHBoxLayout()
        self.connection_label = QLabel("Не подключено")
        self.connection_label.setStyleSheet('color: red')

        button_connect = QPushButton("Подключение")
        button_connect.setFixedSize(100, 50)
        self.ser = button_connect.clicked.connect(self.connect_port)
        if isinstance(self.ser, serial.Serial):
            setup_coords(self.ser)

        button_remove = QPushButton("Новый проект")
        button_remove.setFixedSize(150, 50)
        button_remove.clicked.connect(self.remove_all)

        header.addWidget(button_connect)
        header.addWidget(self.connection_label)
        header.addWidget(button_remove)

        # body
        body = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(8)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        self.table.setVerticalHeaderLabels(["A", "B", "C", "D", "E", "F", "G", "H"])

        for i in range(0,8):
            for j in range(0, 12):
                self.table.setColumnWidth(j, 60)
                item = QTableWidgetItem()
                self.table.itemClicked.connect(self.change_color)
                self.table.setItem(i, j, item)
        self.table.setDisabled(True)

        self.color_buttons = QHBoxLayout()
        body.addWidget(self.table)
        body.addLayout(self.color_buttons)

        # footer
        footer = QHBoxLayout()
        self.edit_button = QPushButton("Задать реагенты")
        self.edit_button.setFixedSize(150, 50)
        self.edit_button.clicked.connect(self.edit)

        self.set_button = QPushButton("Разместить")
        self.set_button.setFixedSize(150, 50)
        self.set_button.clicked.connect(self.setup)

        self.move_button = QPushButton("Переместить")
        self.move_button.setFixedSize(150, 50)
        self.move_button.clicked.connect(self.move)

        self.change_button = QPushButton("Сменить носик")
        self.change_button.setFixedSize(150, 50)
        self.change_button.clicked.connect(self.change)

        footer.addWidget(self.edit_button)
        footer.addWidget(self.set_button)
        footer.addWidget(self.move_button)
        footer.addWidget(self.change_button)

        # main layout assembly
        main_layout.addLayout(header)
        main_layout.addLayout(body)
        main_layout.addLayout(footer)
        self.setLayout(main_layout)

        self.resize(800, 600)

    def connect_port(self):
        print("Подключение...")
        self.ser = establish_connection()
        print(self.ser)
        if isinstance(self.ser, serial.Serial):
            self.connection_label.setText("Подключено")
            self.connection_label.setStyleSheet('color: green')
        else:
            self.connection_label.setText(str(self.ser))

    def remove_all(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def edit(self):
        self.window = EditWindow(self.components)
        self.window.setWindowTitle('Изменить список реагентов')
        self.window.show()


    def setup(self):
        self.mode = 1
        # colors
        if len(self.components) >= self.color_buttons_count:
            while self.color_buttons_count != len(self.components):
                new_comp = self.components[self.color_buttons_count]
                button = QRadioButton(new_comp[0])
                pixmap = QPixmap(100, 100)
                pixmap.fill(QColor(new_comp[1], new_comp[2], new_comp[3], 127))
                button.setIcon(QIcon(pixmap))
                button.setObjectName(f"{new_comp[0]},{new_comp[1]},{new_comp[2]},{new_comp[3]}")
                button.clicked.connect(self.set_color)
                self.color_buttons.addWidget(button)
                self.color_buttons_count += 1
        self.color_buttons.update()

        self.table.setDisabled(False)

        self.edit_button.setDisabled(True)
        self.move_button.setDisabled(True)
        self.change_button.setDisabled(True)

        self.set_button.setText("Завершить")
        self.set_button.clicked.connect(self.finish_setup)
        self.set_button.clicked.disconnect(self.setup)

    def finish_setup(self):
        self.mode = 1
        self.table.setDisabled(True)

        self.edit_button.setDisabled(False)
        self.move_button.setDisabled(False)
        self.change_button.setDisabled(False)

        self.set_button.setText("Разместить")
        self.set_button.clicked.connect(self.setup)
        self.set_button.clicked.disconnect(self.finish_setup)
        self.color_buttons.setEnabled(False)

    def set_color(self):
        data = self.sender().objectName().split(',')
        self.current_color = QColor(int(data[1]), int(data[2]), int(data[3]), 127)
        self.current_comp = data[0]

    def change_color(self):
        if self.mode == 1:
            if self.current_color:
                item = (self.table.item(self.table.currentRow(),self.table.currentColumn()))
                item.setBackground(self.current_color)
                item.setToolTip(self.current_comp)
        if self.mode == 2:
            if self.table.item(self.table.currentRow(), self.table.currentColumn()):
                mess = QMessageBox()
                mess.exec()
            print(2)

    def move(self):
        self.mode = 2
        self.table.setDisabled(False)

        self.edit_button.setDisabled(True)
        self.set_button.setDisabled(True)
        self.change_button.setDisabled(True)

        self.move_button.setText("Завершить")
        self.move_button.clicked.connect(self.finish_move)
        self.move_button.clicked.disconnect(self.move)

    def finish_move(self):
        self.mode = 0
        self.table.setDisabled(True)

        self.edit_button.setDisabled(False)
        self.set_button.setDisabled(False)
        self.change_button.setDisabled(False)

        self.move_button.setText("Переместить")
        self.move_button.clicked.connect(self.move)
        self.move_button.clicked.disconnect(self.finish_move)

    def change(self):
        print("change nose")
        self.ser.write(GO_HOME)
