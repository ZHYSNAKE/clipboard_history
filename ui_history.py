from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

class HistoryTipWindow(QWidget):
    show_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # 窗口设置：无边框、半透明
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(300, 300, 400, 300)
        
        # 样式：深色半透明 + 圆角
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 45, 230);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
            QListWidget {
                background: transparent;
                border: none;
                color: #e0e0e0;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: rgba(100, 150, 255, 80);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 20);
            }
        """)

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # 加载数据
        self.load_history()

        # 连接信号到显示方法
        self.show_signal.connect(self.show_at_cursor)

    def load_history(self):
        from storage import get_history
        rows = get_history()
        self.list_widget.clear()
        for row in rows:
            self.list_widget.addItem(QListWidgetItem(row[1]))

    def show_at_cursor(self):
        """在右上角显示窗口"""
        self.load_history()  # 每次弹出时刷新
        self.setGeometry(50, 50, 400, 200)
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - self.width() - 20, 20)
        self.show()
        self.raise_()
        self.list_widget.setFocus()

    def toggle_visibility(self):
        """显不显示窗口"""
        if self.isVisible():
            self.hide()
        else:
            self.show_at_cursor()