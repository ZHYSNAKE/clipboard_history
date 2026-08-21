import pyperclip
from ui_history import HistoryTipWindow
from PyQt6.QtCore import pyqtSignal, Qt

class KeyEvent(HistoryTipWindow):
    show_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def copy_current_to_clipboard(self):
        item = self.list_widget.currentItem()
        if item:
            pyperclip.copy(item.text())
            # 通知 watcher 跳过下一次记录
            if hasattr(self, 'watcher'):
                self.watcher.skip_next = True
            print(f"📋 剪贴板已更新：{item.text()[:30]}...")

    def move_up(self):
        # 向上移动
        # 把显示的表格指向的指针向上移
        # 如果指针指向的已经是最后一个则不移动
        current_row = self.list_widget.currentRow() # 当前行
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)
            self.copy_current_to_clipboard()

    def move_down(self):  
        # 向下移动
        # 把显示的表格指向的指针向下移
        # 如果指针指向的已经是最后一个则不移动
        current_row = self.list_widget.currentRow() # 当前行
        total = self.list_widget.count()            # 总行数
        current_row = self.list_widget.currentRow()     
        if current_row < total - 1:
            self.list_widget.setCurrentRow(current_row + 1)
            self.copy_current_to_clipboard()

    def del_current(self):
        # 删除当前指针指向的内容并向上移动
        # 如果指针指向的已经是最后一个则向下移动
        from storage import del_by_id  
        current_row = self.list_widget.currentRow() # 当前行
        total = self.list_widget.count()            # 总行数      
        if total > 0:
            id = self.list_widget.item(current_row).data(Qt.ItemDataRole.UserRole)
            print(id)
            del_by_id(id)
            self.list_widget.takeItem(current_row)