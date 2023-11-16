# utils.py

# 示例函数：格式化消息
def format_message(message):
    # 实现消息格式化逻辑
    return f"格式化后的消息: {message}"

# 示例函数：日志记录
def log_message(message):
    # 实现日志记录逻辑
    pass

# 新增添加视频或图片资源的函数
def add_resource(file_id, file_name, tags):
    # 将视频或图片资源添加到数据库的逻辑，通过调用db_interface模块的方法实现
    from db_interface import add_media_to_db
    add_media_to_db(file_id, file_name, tags)
