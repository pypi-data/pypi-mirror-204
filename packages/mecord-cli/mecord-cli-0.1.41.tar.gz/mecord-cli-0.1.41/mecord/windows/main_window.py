from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QPushButton


class IMainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # 继承自QWidget类 创建一个新的类实例(实例化对象))
        self.resize(1280, 720)
        self.setWindowTitle(self.tr('Mecord'))
