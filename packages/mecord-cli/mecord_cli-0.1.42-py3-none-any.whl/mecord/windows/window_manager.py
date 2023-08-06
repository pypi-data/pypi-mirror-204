import os
from pathlib import Path
from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine
from mecord.windows.signal_center import SignalCenter


class WindowManager(QObject):

    def __init__(self):
        super(WindowManager, self).__init__()

        self.main_window = None  # 主面板
        self.main_window_file_name = "main_window.qml"
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.objectCreated.connect(self.qml_win_created)
        self.init_ui()
        self.init_public_listener()

    def __del__(self):
        self.remove_public_listener()

    def qml_win_created(self, obj, url):
        file_name = url.fileName()
        if file_name == self.main_window_file_name:
            self.main_window = obj

    def init_ui(self):
        pass

    def init_public_listener(self):
        try:
            SignalCenter().show_main_window.connect(self.show_main_window)
        except:
            pass

    def remove_public_listener(self):
        try:
            SignalCenter().show_main_window.disconnect(self.show_main_window)
        except:
            pass

    def show_main_window(self):
        if self.main_window == None:
            self.qml_engine.load(":/qml/main_window.qml")
        self.main_window.show()


