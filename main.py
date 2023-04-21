import sys
import contactbook
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    main_window = contactbook.MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
