from telegram import Update
from telegram.ext import CallbackContext

# 处理文本消息的函数
def text_message_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    update.message.reply_text(f'你发送了文本: {text}')

# 新增添加视频或图片资源的函数
def add_resource(file_id, file_name, tags):
    db_interface.add_media_to_db(file_id, file_name, tags)
