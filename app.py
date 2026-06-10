from PyQt6.QtWidgets import QApplication
import sys
from gui.window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()

with open('.\\style\\style.css', 'r', encoding='utf-8') as style:
    app.setStyleSheet(style.read())

sys.exit(app.exec())