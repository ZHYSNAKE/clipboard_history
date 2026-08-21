from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal


class HistoryTipWindow(QFrame):
    show_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("历史剪贴板")
        self.setGeometry(300, 300, 400, 300)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
            }
            QListWidget {
                background: #ffffff;
                border: none;
                color: #000000;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #000000;   /* 黑线分割 */
            }
            QListWidget::item:selected {
                background-color: #e0e8f0;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f0f4f8;
            }
        """)

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
        # 选中最新的一条（第一条）
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
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