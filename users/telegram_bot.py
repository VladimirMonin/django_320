import logging
from django.conf import settings
from users.models import User
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ParseMode
import asyncio

logging.basicConfig(level=logging.INFO)

async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    if args:
        user_uuid = args[0]
        try:
            # Используем параллельное выполнение для работы с базой данных
            user = await asyncio.to_thread(User.objects.get, uuid=user_uuid)
            user.tg_chat_id = str(chat_id)
            await asyncio.to_thread(user.save)
            
            await context.bot.send_message(chat_id=chat_id, text="Привет! Вы успешно подписались на уведомления!")
            logging.info(f'Пользователь {user.username} подписался на уведомления')
        except User.DoesNotExist:
            await context.bot.send_message(chat_id=chat_id, text="Извините, не удалось найти пользователя")
            logging.error(f'Пользователь с UUID {user_uuid} не найден')
    else:
        await context.bot.send_message(chat_id=chat_id, text="Привет! Для подписки на уведомления используйте специальную ссылку из вашего профиля на сайте")

async def run_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', handle_start_command))
    await application.start_polling()
    await application.wait_closed()

if __name__ == "__main__":
    asyncio.run(run_bot())
