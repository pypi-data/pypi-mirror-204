from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from mecord.windows.bind_widget_ui import Ui_BindWidget
from mecord import utils


class BindWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # 继承自QWidget类 创建一个新的类实例(实例化对象))
        self.ui = Ui_BindWidget()
        self.ui.setupUi(self)
        self.init_ui()

    def init_ui(self):
        uuid = utils.generate_unique_id()
        qrcode_str = f"https://main_page.html?action=scanbind&deviceId={uuid}"
        qrcode_file = utils.create_qrcode(qrcode_str)
        self.ui.lb_devide_id.setText(uuid)
        pixmap = QPixmap(qrcode_file).scaled(self.ui.lb_qr_code.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.ui.lb_qr_code.setPixmap(pixmap)



