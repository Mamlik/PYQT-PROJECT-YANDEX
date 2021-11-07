from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QWidget

class User_Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('user_interface.ui', self)
        self.setWindowTitle('Главная Страница-YandexEda')