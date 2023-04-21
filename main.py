import sys
import contactbook
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
main_window = contactbook.MainWindow()
main_window.show()
sys.exit(app.exec())
