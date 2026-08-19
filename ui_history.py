import sys
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
import pyperclip
import json

class HistoryTipWindow(QWidget):
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

        # 加载假数据
        self.load_demo_data()

        # 默认隐藏
        self.hide()

    def load_demo_data(self):
        """加载示例数据，用来测试界面"""
        demo_items = [
            "Hello, 这是第一条历史",
            "def hello_world(): print('hello')",
            "https://github.com/your/repo",
            "你好，这是第四条内容",
            "最后一条历史记录，用于测试滚动效果"
        ]
        for text in demo_items:
            self.list_widget.addItem(QListWidgetItem(text))

    def show_at_cursor(self):
        """在鼠标位置附近显示窗口"""
        cursor_pos = QCursor.pos()
        self.move(cursor_pos.x() - 200, cursor_pos.y() - 50)
        self.show()
        self.raise_()
        self.activateWindow()

    




# 测试入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistoryTipWindow()
    window.show_at_cursor()  # 测试显示
    sys.exit(app.exec())