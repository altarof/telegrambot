from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from resource_manager import export_resource_data
from config import ADMINS
import os

def start(update: Update, context: CallbackContext) -> None:
    ad1_title = os.getenv('AD1')
    ad1_link = os.getenv('AD1_link')
    ad2_title = os.getenv('AD2')
    ad2_link = os.getenv('AD2_link')

    keyboard = [
        [InlineKeyboardButton("我的账户 🙋‍♂️", callback_data='my_account')],
        [InlineKeyboardButton("资源搜索 🔍", callback_data='search_resources')],
        [InlineKeyboardButton("随机资源 🎲", callback_data='random_resources')],
        [InlineKeyboardButton("热门标签 🔥", callback_data='hot_tags')]
    ]

    if ad1_title and ad1_title.lower() != 'off':
        keyboard.append([InlineKeyboardButton(ad1_title, url=ad1_link)])
    if ad2_title and ad2_title.lower() != 'off':
        keyboard.append([InlineKeyboardButton(ad2_title, url=ad2_link)])

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('功能菜单', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('这里是帮助信息。')

def ziyuan_command(update: Update, context: CallbackContext) -> None:
    context.chat_data['record_resources'] = True

    if update.message:
        update.message.reply_text('现在可以上传资源了。请上传图片或视频，并添加合适的标签。')
    elif update.channel_post:
        update.channel_post.reply_text('现在可以上传资源了。请上传图片或视频，并添加合适的标签。')

def ziyuanshuju_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    if user_id in ADMINS:
        resource_data = export_resource_data()
        
        if not resource_data:
            update.message.reply_text('没有资源数据可供导出。')
            return
        
        with open('resource_data.txt', 'w', encoding='utf-8') as file:
            file.writelines(resource_data)
        
        with open('resource_data.txt', 'rb') as file:
            context.bot.send_document(chat_id=user_id, document=file, filename='resource_data.txt')
    else:
        update.message.reply_text('抱歉，你没有权限执行这个操作。')

def account_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = query.from_user
    user_name = user.full_name
    user_id = user.id
    remaining_time = "30天"

    buy_card_link = os.getenv('BUY_CARD')
    account_recharge_link = os.getenv('ACCOUNT_RECHARGE')
    ad1_title = os.getenv('AD1')
    ad1_link = os.getenv('AD1_link')
    ad2_title = os.getenv('AD2')
    ad2_link = os.getenv('AD2_link')

    keyboard = []
    if buy_card_link:
        keyboard.append([InlineKeyboardButton("购买卡密", url=buy_card_link)])
    if account_recharge_link:
        keyboard.append([InlineKeyboardButton("账户充值", url=account_recharge_link)])
    if ad1_title and ad1_title.lower() != 'off':
        keyboard.append([InlineKeyboardButton(ad1_title, url=ad1_link)])
    if ad2_title and ad2_title.lower() != 'off':
        keyboard.append([InlineKeyboardButton(ad2_title, url=ad2_link)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"用户名称: {user_name}\n用户ID: {user_id}\n剩余时长: {remaining_time}"
    query.edit_message_text(text=message_text, reply_markup=reply_markup)

def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data

    if query_data == 'my_account':
        account_menu(update, context)
    # Add more callback handling logic here as needed




-config.py
from dotenv import load_dotenv
import os

load_dotenv()  # 读取.env文件中的环境变量

TOKEN = os.getenv('TELEGRAM_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# 从环境变量获取管理员ID，并转换为整数列表
ADMINS = [
    int(admin_id.strip()) for admin_id in os.getenv('ADMIN_IDS', '').split(',')
]

