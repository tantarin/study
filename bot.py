import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from game_logic import GameManager
from kafka_cards import KAFKA_CARDS

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация игрового менеджера
game_manager = GameManager()

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        update.effective_message.reply_text(
            "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
        )

def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Начать обучение", callback_data='start_learning')],
        [InlineKeyboardButton("Правила игры", callback_data='rules')],
        [InlineKeyboardButton("Моя статистика", callback_data='stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "👋 Привет! Я бот для изучения Apache Kafka в игровом формате.\n\n"
        "Выберите действие:",
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
        
        if query.data == 'start_learning':
            query.message.reply_text(
                "🎮 Отлично! Давайте начнем изучение Kafka.\n\n"
                "Вы будете изучать теорию по карточкам, каждая из которых содержит подробное объяснение темы.\n\n"
                "Готовы начать?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Да, начинаем!", callback_data='start_cards')]
                ])
            )
        elif query.data == 'rules':
            query.message.reply_text(
                "📖 Как это работает:\n\n"
                "1. Каждая карточка содержит подробное объяснение темы\n"
                "2. Карточки показываются в случайном порядке\n"
                "3. Вы можете изучать карточки в своем темпе\n\n"
                "Удачи в обучении! 🚀"
            )
        elif query.data == 'stats':
            progress = game_manager.get_level_progress(user_id)
            query.message.reply_text(
                f"📊 Ваш прогресс:\n\n"
                f"Изучено карточек: {progress['cards_viewed']} из {progress['total_cards']}"
            )
        elif query.data == 'start_cards':
            show_question(update, context, user_id)
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