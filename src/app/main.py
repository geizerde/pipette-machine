from PySide6.QtWidgets import QApplication, QPushButton, QHeaderView, QVBoxLayout, QHBoxLayout, QTableWidget, QWidget, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # header
        header = QHBoxLayout()
        label = QLabel("Подключено")
        button = QPushButton("Подключение")
        button.setFixedSize(100, 50)
        button.clicked.connect(self.start_work)

        header.addWidget(button)
        header.addWidget(label)

        # body
        body = QHBoxLayout()
        table = QTableWidget()

        colors = [("Red", "#FF0000"),
                  ("Green", "#00FF00"),
                  ("Blue", "#0000FF"),
                  ("Black", "#000000"),
                  ("White", "#FFFFFF"),
                  ("Electric Green", "#41CD52"),
                  ("Dark Blue", "#222840"),
                  ("Yellow", "#F9E56d")]

        table.setRowCount(10)
        table.setColumnCount(15)
        table.setHorizontalHeaderLabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        for i in range(0,15):
            table.setColumnWidth(i,50)
        body.addWidget(table)

        # footer
        footer = QHBoxLayout()
        edit_button = QPushButton("Редактировать")
        edit_button.setFixedSize(150, 50)
        set_button = QPushButton("Разместить")
        set_button.setFixedSize(150, 50)
        move_button = QPushButton("Переместить")
        move_button.setFixedSize(150, 50)
        change_button = QPushButton("Сменить носик")
        change_button.setFixedSize(150, 50)

        button.clicked.connect(self.start_work)
        footer.addWidget(edit_button)
        footer.addWidget(set_button)
        footer.addWidget(move_button)
        footer.addWidget(change_button)

        # main layout assembly
        main_layout.addLayout(header)
        main_layout.addLayout(body)
        main_layout.addLayout(footer)
        self.setLayout(main_layout)

        self.resize(800, 600)

    def start_work(self):
        print("Кнопка нажата!")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle('Автоматический пипет дозатор')
    window.show()
    app.exec()