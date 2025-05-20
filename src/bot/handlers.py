import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from src.cards import (
    JAVA_CORE_CARDS,
    SPRING_CARDS,
    DATABASE_CARDS,
    DOCKER_K8S_CARDS
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Словарь для хранения состояния пользователей
user_states = {}

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        update.effective_message.reply_text(
            "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
        )

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Java Core", callback_data='java_core')],
        [InlineKeyboardButton("Spring Framework", callback_data='spring')],
        [InlineKeyboardButton("Базы данных", callback_data='database')],
        [InlineKeyboardButton("Docker & Kubernetes", callback_data='docker_k8s')],
        [InlineKeyboardButton("Статистика", callback_data='stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Привет! Я бот для подготовки к собеседованиям по Java и смежным технологиям.\n'
        'Выберите раздел для изучения:',
        reply_markup=reply_markup
    )

def show_question(update: Update, context: CallbackContext, user_id: int):
    """Показывает текущую карточку с теорией пользователю"""
    try:
        question = game_manager.get_current_question(user_id)
        if not question:
            if update.callback_query:
                update.callback_query.message.reply_text(
                    "Поздравляем! Вы изучили все доступные карточки! 🎉\n"
                    "Новые карточки будут добавлены в ближайшее время."
                )
            else:
                update.message.reply_text(
                    "Поздравляем! Вы изучили все доступные карточки! 🎉\n"
                    "Новые карточки будут добавлены в ближайшее время."
                )
            return

        progress = game_manager.get_level_progress(user_id)
        
        message_text = (
            f"📚 Теория (Карточка {progress['cards_viewed'] + 1} из {progress['total_cards']})\n\n"
            f"{question.theory}\n\n"
            "Нажмите 'Следующая карточка', чтобы продолжить обучение."
        )
        keyboard = [[InlineKeyboardButton("Следующая карточка", callback_data='next_card')]]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            update.callback_query.message.reply_text(
                text=message_text,
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in show_question: {e}")
        if update.callback_query:
            update.callback_query.message.reply_text(
                "Произошла ошибка при отображении карточки. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
            )
        else:
            update.message.reply_text(
                "Произошла ошибка при отображении карточки. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
            )

def button_handler(update: Update, context: CallbackContext):
    """Обработчик нажатий на кнопки"""
    try:
        query = update.callback_query
        if not query:
            return
            
        user_id = query.from_user.id
        
        if query.data == 'java_core':
            show_question(update, context, user_id)
        elif query.data == 'spring':
            show_question(update, context, user_id)
        elif query.data == 'database':
            show_question(update, context, user_id)
        elif query.data == 'docker_k8s':
            show_question(update, context, user_id)
        elif query.data == 'stats':
            progress = game_manager.get_level_progress(user_id)
            query.message.reply_text(
                f"📊 Ваш прогресс:\n\n"
                f"Изучено карточек: {progress['cards_viewed']} из {progress['total_cards']}"
            )
        elif query.data == 'next_card':
            state = game_manager.get_user_state(user_id)
            state.next_card()
            show_question(update, context, user_id)
    except Exception as e:
        logger.error(f"Error in button_handler: {e}")
        if update.callback_query:
            update.callback_query.message.reply_text(
                "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
            )

def main():
    """Запуск бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Добавляем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_error_handler(error_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 