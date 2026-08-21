import sys
import json
import keyboard
import pyperclip
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from listener import KeyEvent
from storage import init_db, save_history


class ClipboardWatcher:
    def __init__(self):
        self.last_text = ""
        self.skip_next = False

    def check(self):
        # 上下切换的时候不把指定内容加入到表里
        if self.skip_next:
            self.skip_next = False
            # 还要同步更新 last_text 为当前剪贴板内容，防止后续误判
            self.last_text = pyperclip.paste()
            return

        text = pyperclip.paste()
        if text and text != self.last_text:
            self.last_text = text
            save_history(text)
            print(f"[已记录] {text[:30]}...")

def main():
    init_db()
    print("数据库已就绪")

    app = QApplication(sys.argv)
    watcher = ClipboardWatcher()
    window = KeyEvent()
    window.watcher = watcher
    print("窗口已创建")

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # 注册全局热键（呼出窗口）
    keyboard.add_hotkey(config["hotkey_prev"], window.show_signal.emit)
    keyboard.add_hotkey(config["hotkey_next"], window.show_signal.emit)

    # 切换窗口显示/隐藏的线程
    window.toggle_signal.connect(window.toggle_visibility)
    keyboard.add_hotkey(config["hotkey_show"], window.toggle_signal.emit)

    # 退出程序的线程
    window.close_signal.connect(app.quit)
    keyboard.add_hotkey(config["hotkey_close"], window.close_signal.emit)

    # 启动轮询
    timer = QTimer()
    timer.timeout.connect(watcher.check)
    timer.start(config.get("save_time", 200))
    print("剪贴板自动记录已启动")

    print("✅ 所有热键已注册")
    print(f"📌 按 {config['hotkey_prev']}/{config['hotkey_next']} 呼出历史列表")
    print(f"📌 按 {config['hotkey_show']} 切换窗口显示/隐藏")
    print(f"📌 按 {config['hotkey_close']} 退出程序")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()