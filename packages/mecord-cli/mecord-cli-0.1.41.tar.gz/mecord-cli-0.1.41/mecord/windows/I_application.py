from PySide6.QtWidgets import QApplication
from mecord.windows.window_manager import WindowManager


class IApplication(QApplication):

    def __init__(self, args):
        super().__init__(args)
        self.windows_manager = WindowManager()
