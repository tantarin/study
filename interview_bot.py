import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv
from java_core_cards import JAVA_CORE_CARDS
from spring_cards import SPRING_CARDS

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения состояния пользователей
user_states = {}

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Java Core", callback_data='java_core')],
        [InlineKeyboardButton("Spring Framework", callback_data='spring')],
        [InlineKeyboardButton("Статистика", callback_data='stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Привет! Я бот для подготовки к собеседованиям по Java.\n'
        'Выберите раздел для изучения:',
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    query.answer()
    
    if query.data == 'java_core':
        show_java_core_menu(update, context)
    elif query.data == 'spring':
        show_spring_menu(update, context)
    elif query.data == 'stats':
        show_stats(update, context)
    elif query.data == 'back':
        # Возвращаемся в главное меню
        keyboard = [
            [InlineKeyboardButton("Java Core", callback_data='java_core')],
            [InlineKeyboardButton("Spring Framework", callback_data='spring')],
            [InlineKeyboardButton("Статистика", callback_data='stats')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(
            'Выберите раздел для изучения:',
            reply_markup=reply_markup
        )
    elif query.data.startswith('java_topic_'):
        show_java_topic(update, context, query.data.split('_')[2])
    elif query.data.startswith('spring_topic_'):
        show_spring_topic(update, context, query.data.split('_')[2])

def show_java_core_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем Java Core"""
    keyboard = []
    for i, card in enumerate(JAVA_CORE_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'java_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по Java Core:",
        reply_markup=reply_markup
    )

def show_spring_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем Spring"""
    keyboard = []
    for i, card in enumerate(SPRING_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'spring_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по Spring:",
        reply_markup=reply_markup
    )

def show_java_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Java Core"""
    card = JAVA_CORE_CARDS[int(topic_index)]
    message = f"*{card.text}*\n\n"
    message += f"{card.theory}\n\n"
    message += f"*Практические примеры:*\n{card.explanation}"
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='java_core')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_spring_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Spring"""
    card = SPRING_CARDS[int(topic_index)]
    message = f"*{card.text}*\n\n"
    message += f"{card.theory}\n\n"
    message += f"*Практические примеры:*\n{card.explanation}"
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='spring')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_stats(update: Update, context: CallbackContext) -> None:
    """Показать статистику изучения"""
    user_id = update.callback_query.from_user.id
    if user_id not in user_states:
        user_states[user_id] = {'java_core': set(), 'spring': set()}
    
    java_core_learned = len(user_states[user_id]['java_core'])
    spring_learned = len(user_states[user_id]['spring'])
    
    message = f"*Ваша статистика:*\n\n"
    message += f"Java Core: {java_core_learned}/{len(JAVA_CORE_CARDS)} тем\n"
    message += f"Spring: {spring_learned}/{len(SPRING_CARDS)} тем"
    
    keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def main() -> None:
    """Запуск бота"""
    # Получение токена из переменных окружения
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error("Не найден токен Telegram бота!")
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
    updater.idle()

if __name__ == '__main__':
    main() 