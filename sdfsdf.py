import sys

from PyQt5.QtWidgets import QApplication

from main import MainWindow1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow1()
    main_win.show()
    sys.exit(app.exec())