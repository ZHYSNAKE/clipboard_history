from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal


class HistoryTipWindow(QFrame):
    show_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # 窗口设置：无边框 + 不透明
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        # 不启用透明，背景色直接生效
        self.setGeometry(300, 300, 400, 300)
        
        # 样式：浅蓝 + 圆角 + 黑色文字
        self.setStyleSheet("""
            QFrame {
                background-color: #e8f4fd;      /* 浅蓝色 */
                border-radius: 40px;            /* 大圆角 */
                border: 1px solid rgba(100, 180, 255, 80);
            }
            QListWidget {
                background: transparent;
                border: none;
                color: #000000;                /* ← 纯黑文字 */
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 10px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #7bb8e0;      /* 选中浅蓝 */
                color: white;
            }
            QListWidget::item:hover {
                background-color: #c5e0f5;      /* 悬停浅蓝 */
            }"""
        )

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.load_history()
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
        """切换窗口显示/隐藏"""
        if self.isVisible():
            self.hide()
        else:
            self.show_at_cursor()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = HistoryTipWindow()
    window.show_at_cursor()
    sys.exit(app.exec())