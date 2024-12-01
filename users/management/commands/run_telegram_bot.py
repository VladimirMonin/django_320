from django.core.management.base import BaseCommand
from users.telegram_bot import run_bot
import threading

class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write('Запуск Telegram бота...')
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
