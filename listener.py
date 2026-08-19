import json
import pyperclip

def key_press_event(self, key):
        """处理键盘事件：上下切换、默认Enter复制、Esc关闭"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            current_row = self.list_widget.currentRow() # 当前行
            total = self.list_widget.count()            # 总行数

            if key == data["hotkey_prev"]:
                # 向上移动
                # 把显示的表格指向的指针向上移
                # 如果指针指向的已经是最后一个则不移动
                if current_row > 0:
                    self.list_widget.setCurrentRow(current_row - 1) 
            elif key == data["hotkey_next"]:
                # 向下移动
                # 把显示的表格指向的指针向下移
                # 如果指针指向的已经是最后一个则不移动
                if current_row < total - 1:
                    self.list_widget.setCurrentRow(current_row + 1)
            elif key == data["hotkey_delete"]:
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
            elif key == data["hotkey_enter"]:
                # 选择当前指针指向的内容到剪贴板
                # 并把其添加到表格最下方并且指针也指向过去
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