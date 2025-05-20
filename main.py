import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from src.bot.handlers import (
    start,
    button_handler
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Запуск бота"""
    # Загрузка переменных окружения
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("Не найден токен Telegram бота в переменных окружения")
        return
    
    # Создание Updater и передача ему токена бота
    updater = Updater(token)
    
    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    
    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    # Запуск бота
    updater.start_polling()
    logger.info("Бот запущен")
    
    # Остановка бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main() 