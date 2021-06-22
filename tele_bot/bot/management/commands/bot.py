from django.core.management.base import BaseCommand
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from django.conf import settings
from .common import register_handlers_common
from .browse import register_handlers_browse
from .questions import register_handlers_legal

# Объявление и инициализация объектов бота и диспетчера
my_bot = Bot(token=settings.TOKEN)
dp = Dispatcher(my_bot, storage=MemoryStorage())

logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(my_bot: Bot):
    commands = [
        BotCommand(command="/browse", description="Поиск по исковым заявлениям"),
        BotCommand(command="/questions", description="Поиск формат вопрос-ответ"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await my_bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting my_bot")

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_browse(dp)
    register_handlers_legal(dp)

    # Установка команд бота
    await set_commands(my_bot)

    # Запуск поллинга
    await dp.start_polling()


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        asyncio.run(main())

