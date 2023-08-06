from PySide6.QtCore import QObject, Signal

from mecord.public_tools.decorator_tools import singleton


@singleton
class SignalCenter(QObject):
    """
    该模块提供所有全局信号，降低各个模块间的耦合
    警告：使用全局信号时，记得要手动disconnect
    例子：signal = pyqSignal(str)
    """
    show_main_window = Signal()  #show main window
    show_bind_window = Signal()

