
from PySide6.QtCore import QObject, Signal
from mecord.windows.main_window import IMainWindow
from mecord.windows.signal_center import SignalCenter
from mecord.windows.bind_widget import BindWidget


class WindowManager(QObject):

    def __init__(self):
        super(WindowManager, self).__init__()

        self.main_window = None  # 主面板
        self.bind_window = None  # 扫码绑定窗口
        self.init_public_listener()

    def __del__(self):
        self.remove_public_listener()

    def init_public_listener(self):
        try:
            SignalCenter().show_main_window.connect(self.show_main_window)
            SignalCenter().show_bind_window.connect(self.show_bind_window)
        except:
            pass

    def remove_public_listener(self):
        try:
            SignalCenter().show_main_window.disconnect(self.show_main_window)
            SignalCenter().show_bind_window.disconnect(self.show_bind_window)
        except:
            pass

    def show_main_window(self):
        if self.main_window == None:
            self.main_window = IMainWindow()
        self.main_window.show()

    def show_bind_window(self):
        if self.bind_window == None:
            self.bind_window = BindWidget()
        self.bind_window.show()

