import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Тест - Работает!")
window.setGeometry(100, 100, 600, 400)

label = QLabel("<h1>PyQt6 работает!</h1><p>Теперь можно запускать main.py</p>", window)
label.setGeometry(50, 50, 500, 100)
label.setStyleSheet("color: white; font-size: 14px;")

window.setStyleSheet("background-color: #23232d;")
window.show()
app.exec()