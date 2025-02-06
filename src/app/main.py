from PySide6.QtWidgets import QApplication

from src.app.windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle('Автоматический пипет дозатор')
    window.show()
    app.exec()