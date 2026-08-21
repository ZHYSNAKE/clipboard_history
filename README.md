# 一个自动记录历史剪切板的小工具

默认按 Ctrl + Shift + W和 Ctrl + Shift + S切换历史剪切板  
默认按 Ctrl + Shift + D 删除所选数据  
默认按 Ctrl + Shift + Q 退出  
默认每200ms记录一次剪贴板的内容，如果200ms内多次复制只会复制最后一次  

PS:我这个按键监听是全局监听，所以你不选中页面也能使，而且最好不要绑方向键上下，会冲突  

config.json:  
"hotkey_prev"    - 向上切换键  
"hotkey_next"    - 向下切换键  
"hotkey_delete": - 删除键  
"hotkey_close":  - 关闭键  
"max_history":   - 一次最多显示内容（未实装） 
"save_time":     - 多少毫秒记录一次  

