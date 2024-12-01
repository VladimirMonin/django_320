from django.apps import AppConfig
import threading

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from users.telegram_bot import run_bot

        # Функция для запуска бота в отдельном потоке
        def start_bot():
            import asyncio
            asyncio.run(run_bot())

        # Запускаем поток
        bot_thread = threading.Thread(target=start_bot, name="TelegramBot")
        bot_thread.daemon = True
        bot_thread.start()
