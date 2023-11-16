# resource_manager.py
import sqlite3

# 创建表
def create_table():
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        file_id TEXT,
        file_name TEXT,
        tags TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# 添加新资源
def add_resource(file_id, file_name, tags):
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO resources (file_id, file_name, tags) 
    VALUES (?, ?, ?)
    ''', (file_id, file_name, tags))
    conn.commit()
    cursor.close()
    conn.close()

# 修改资源
def update_resource(resource_id, file_id, file_name, tags):
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE resources
    SET file_id = ?, file_name = ?, tags = ?
    WHERE id = ?
    ''', (file_id, file_name, tags, resource_id))
    conn.commit()
    cursor.close()
    conn.close()

# 导出资源数据
def export_resource_data():
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources')
    rows = cursor.fetchall()
    data = [f"{row[2]}-{row[1]}-{row[3]}\n" for row in rows]
    cursor.close()
    conn.close()
    return data

# 删除资源
def remove_resource(resource_id):
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    conn.commit()
    cursor.close()
    conn.close()

# 搜索资源
def search_resource(tag):
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources WHERE tags LIKE ?', ('%' + tag + '%',))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

create_table()

