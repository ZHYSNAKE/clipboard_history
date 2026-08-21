import sqlite3

def init_db():
    """创建数据库"""
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_history(text):
    """插入数据"""
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO history (content)
        VALUES (?)
        """, (text,) 
    )
    conn.commit()
    conn.close()


def get_history():
    """获取最近几条历史记录（默认100）"""
    import json
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        """
        SELECT * 
        FROM history 
        ORDER BY timestamp DESC
        LIMIT ?
        """,(data["max_history"],)
    )  
    rows = c.fetchall()
    conn.close()
    return rows

def del_history():
    """删除超时历史记录（默认1h）"""
    import json
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM history 
        WHERE timestamp < datetime('now', '-' || ? || ' minutes')
        """,(data["expire_minutes"],)
    )
    conn.commit()
    print("已删除")
    conn.close()

def del_by_id(id):
    """按id删除历史记录"""
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM history 
        WHERE id=?
        """,(id,)
    )
    conn.commit()
    conn.close()