import sys
import json
import keyboard
from PyQt6.QtWidgets import QApplication
from listener import start_listener, KeyEvent
from storage import init_db


def main():
    """
        1.创建数据库
        2.创建窗口
        3.开启事件监听，监听要输入的时候（输入光标闪烁）
        4.根据按键反馈
    """
    #----- 创建数据库 -----
    init_db()
    print("数据库已就绪")
    
    #----- 创建窗口 -----
    app = QApplication(sys.argv)
    window = KeyEvent()
    print("窗口已创建")
    
    #----- 开启事件监听 -----
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f) 
    # 按上下切换键显示ui
    keyboard.add_hotkey(config["hotkey_prev"], window.show_signal.emit)
    keyboard.add_hotkey(config["hotkey_next"], window.show_signal.emit)

    #----- 按键反馈 -----
    keyboard.add_hotkey(config["hotkey_prev"], window.move_up)
    keyboard.add_hotkey(config["hotkey_next"], window.move_down)
    keyboard.add_hotkey(config["hotkey_delete"], window.del_current)
    keyboard.add_hotkey(config["hotkey_enter"], window.confirm_and_copy)

    #----- 启动剪贴板监听（在后台） -----
    start_listener()
    
    keyboard.add_hotkey(config["hotkey_show"], window.toggle_visibility)
    keyboard.add_hotkey(config["hotkey_close"], app.quit)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()