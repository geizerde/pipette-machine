import numpy as np
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

class EditWindow(QWidget):
    options: QVBoxLayout
    add_input: QLineEdit
    components: []

    def __init__(self, components: []):
        super().__init__()
        self.components = components
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.options = QListWidget()

        if self.components:
            for c in self.components:
                option = QListWidgetItem()
                option.setText(c[0])
                option.setBackground(QColor(c[1], c[2], c[3], 127))

                self.options.addItem(option)

        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("Введите название реагента")
        self.add_input.setFixedSize(400, 50)
        add_button = QPushButton("+ Добавить реагент")
        add_button.setFixedSize(400, 50)
        add_button.clicked.connect(self.add_component)

        main_layout.addWidget(self.options)
        main_layout.addWidget(self.add_input)
        main_layout.addWidget(add_button)

        self.setLayout(main_layout)

        self.resize(400, 400)

    def add_component(self):
        component = str(self.add_input.text())
        red = np.random.choice(range(0, 256, 10))
        green = np.random.choice(range(0, 256, 10))
        blue = np.random.choice(range(0, 256, 10))

        self.components.append([component, red, green, blue])

        new_option = QListWidgetItem()
        new_option.setText(component)
        new_option.setBackground(QColor(red, green, blue, 127))

        self.options.addItem(new_option)

