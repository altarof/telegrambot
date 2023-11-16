# 导入需要的库
from telegram import Update  # 导入Update类
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext  # 添加 CallbackContext
import logging
import os

# 导入其他模块
from commands import start, help_command, callback_handler, ziyuan_command, ziyuanshuju_command
from message_handlers import text_message_handler
from resource_manager import add_resource
from config import TOKEN

# 设置日志记录，帮助调试
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# 在这里打印 Token 以确认其值
print("Loaded Token:", TOKEN)

# 添加处理频道消息的函数
def handle_channel_broadcast(update: Update, context: CallbackContext) -> None:
    # 检查是否是 /ziyuan 命令
    if update.channel_post.text == "/ziyuan":
        ziyuan_command(update, context)  # 调用 /ziyuan 的处理函数

# 新增处理视频和图片消息的函数
def handle_media_message(update: Update, context: CallbackContext) -> None:
    if context.chat_data.get('record_resources'):
        file_id = None
        file_name = None
        tags = update.message.caption or "无标签"

        # 检查消息类型并获取相应的文件ID
        if update.message.video:
            file_id = update.message.video.file_id
            file_name = update.message.video.file_name
            add_resource(file_id, file_name, tags)  # 如果找到视频的文件ID，则添加到数据库
        elif update.message.photo:
            file_id = update.message.photo[-1].file_id  # 获取最高分辨率的图片
            file_name = update.message.photo[-1].file_name
            add_resource(file_id, file_name, tags)  # 如果找到图片的文件ID，则添加到数据库

# 定义 main 函数，用于启动机器人
def main():
    # 创建 updater 对象并传入 Bot 的 Token
    updater = Updater(token=TOKEN, use_context=True)

    # 获取 dispatcher 来注册处理器
    dp = updater.dispatcher

    # 添加基本的命令处理器
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # 添加 /ziyuan 命令处理器
    dp.add_handler(CommandHandler("ziyuan", ziyuan_command))

    # 添加处理/ziyuanshuju命令的处理器
    dp.add_handler(CommandHandler("ziyuanshuju", ziyuanshuju_command))

    # 添加处理频道消息的处理器
    dp.add_handler(MessageHandler(Filters.update.channel_posts, handle_channel_broadcast))

    # 添加文本消息处理器
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message_handler))

    # 添加回调查询处理器
    dp.add_handler(CallbackQueryHandler(callback_handler))

    # 添加处理视频和图片消息的处理器
    dp.add_handler(MessageHandler(Filters.video | Filters.photo, handle_media_message))

    # 开始轮询，以接收新的更新
    updater.start_polling()

    # 运行程序直到被中断
    updater.idle()

# 程序入口点
if __name__ == '__main__':
    main()


