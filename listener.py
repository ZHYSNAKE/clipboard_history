import json
import pyperclip
from storage import save_history
from ui_history import HistoryTipWindow
import keyboard

class KeyEvent(HistoryTipWindow):
    def move_up(self):
        # 向上移动
        # 把显示的表格指向的指针向上移
        # 如果指针指向的已经是最后一个则不移动
        current_row = self.list_widget.currentRow() # 当前行
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)

    def move_down(self):  
        # 向下移动
        # 把显示的表格指向的指针向下移
        # 如果指针指向的已经是最后一个则不移动
        current_row = self.list_widget.currentRow() # 当前行
        total = self.list_widget.count()            # 总行数
        current_row = self.list_widget.currentRow()     
        if current_row < total - 1:
            self.list_widget.setCurrentRow(current_row + 1)

    def del_current(self):
        # 删除当前指针指向的内容并向上移动
        # 如果指针指向的已经是最后一个则向下移动  
        current_row = self.list_widget.currentRow() # 当前行
        total = self.list_widget.count()            # 总行数      
        if total > 0:
            self.list_widget.takeItem(current_row)
            # 如果删除后列表空了，不做特殊处理
            # 如果删除后还有项，选中下一行（如果当前行超出范围则选中最后一行）
            new_total = self.list_widget.count()
            if new_total > 0:
                if current_row >= new_total:
                    self.list_widget.setCurrentRow(new_total - 1)
                else:
                    self.list_widget.setCurrentRow(current_row)

    def confirm_and_copy(self):
        # 选择当前指针指向的内容到剪贴板
        # 并把其添加到表格最下方并且指针也指向过去
        current_row = self.list_widget.currentRow() # 当前行
        item = self.list_widget.currentItem()
        if item:
            text = item.text()
            pyperclip.copy(text)
            print(f"已复制：{text[:30]}...")
            # 把当前项移到最下方（表示“最近使用”）
            self.list_widget.takeItem(current_row)
            self.list_widget.addItem(text)
            self.list_widget.setCurrentRow(self.list_widget.count() - 1)
            self.hide()  # 或者不隐藏，让用户继续选择


def key_press_event(self, key):
        """处理键盘事件：上下切换、默认Enter复制、Esc关闭"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            current_row = self.list_widget.currentRow() # 当前行
            total = self.list_widget.count()            # 总行数

            if key == config["hotkey_prev"]:
                # 向上移动
                # 把显示的表格指向的指针向上移
                # 如果指针指向的已经是最后一个则不移动
                if current_row > 0:
                    self.list_widget.setCurrentRow(current_row - 1) 
            elif key == config["hotkey_next"]:
                # 向下移动
                # 把显示的表格指向的指针向下移
                # 如果指针指向的已经是最后一个则不移动
                if current_row < total - 1:
                    self.list_widget.setCurrentRow(current_row + 1)
            elif key == config["hotkey_delete"]:
                # 删除当前指针指向的内容并向上移动
                # 如果指针指向的已经是最后一个则向下移动
                if total > 0:
                    self.list_widget.takeItem(current_row)
                    # 如果删除后列表空了，不做特殊处理
                    # 如果删除后还有项，选中下一行（如果当前行超出范围则选中最后一行）
                    new_total = self.list_widget.count()
                    if new_total > 0:
                        if current_row >= new_total:
                            self.list_widget.setCurrentRow(new_total - 1)
                        else:
                            self.list_widget.setCurrentRow(current_row)
            elif key == config["hotkey_enter"]:
                # 选择当前指针指向的内容到剪贴板
                # 并把其添加到表格最下方并且指针也指向过去
                current_row = self.list_widget.currentRow() # 当前行
                item = self.list_widget.currentItem()
                if item:
                    text = item.text()
                    pyperclip.copy(text)
                    print(f"已复制：{text[:30]}...")
                    # 把当前项移到最下方（表示“最近使用”）
                    self.list_widget.takeItem(current_row)
                    self.list_widget.addItem(text)
                    self.list_widget.setCurrentRow(self.list_widget.count() - 1)
                    self.hide()  # 或者不隐藏，让用户继续选择
                
        
        except FileNotFoundError:
            print(f"错误：找不到配置文件 config.json")
            return None
        except json.JSONDecodeError:
            print("错误：配置文件不是合法的 JSON 格式")
            return None
        except Exception as e:
            print(f"发生未知错误：{e}")
            return None
        
def on_copy():
    text = pyperclip.paste()

    if text or text.strip():
        save_history(text)
        print(f"[已记录] {text[:30]}...")
    
def start_listener():
    # 注册热键
    keyboard.add_hotkey('ctrl+c', on_copy)
    print("剪贴板监听已启动，按 Ctrl+C 复制内容即可记录")
