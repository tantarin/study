import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from src.models import Question
from src.cards import (
    JAVA_CORE_CARDS,
    SPRING_CARDS,
    DATABASE_CARDS,
    DOCKER_K8S_CARDS,
    ALGORITHMS_CARDS
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
        [InlineKeyboardButton("Алгоритмы", callback_data='algorithms')],
        [InlineKeyboardButton("Статистика", callback_data='stats')],
        [InlineKeyboardButton("🔄 Старт", callback_data='restart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        update.callback_query.edit_message_text(
            'Привет! Я бот для подготовки к собеседованиям по Java и смежным технологиям.\n'
            'Выберите раздел для изучения:',
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            'Привет! Я бот для подготовки к собеседованиям по Java и смежным технологиям.\n'
            'Выберите раздел для изучения:',
            reply_markup=reply_markup
        )

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

def show_database_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем по базам данных"""
    keyboard = []
    for i, card in enumerate(DATABASE_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'database_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по базам данных:",
        reply_markup=reply_markup
    )

def show_docker_k8s_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем по Docker и Kubernetes"""
    keyboard = []
    for i, card in enumerate(DOCKER_K8S_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'docker_k8s_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по Docker и Kubernetes:",
        reply_markup=reply_markup
    )

def show_algorithms_menu(update: Update, context: CallbackContext) -> None:
    """Показывает меню алгоритмов"""
    query = update.callback_query
    query.answer()
    
    keyboard = []
    for i, card in enumerate(ALGORITHMS_CARDS):
        keyboard.append([InlineKeyboardButton(
            f"{i+1}. {card.text}",
            callback_data=f"algo_{i}"
        )])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите тему по алгоритмам:",
        reply_markup=reply_markup
    )

def show_card(update: Update, context: CallbackContext, card: Question) -> None:
    """Показывает карточку с вопросом и ответом"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📝 Теория", callback_data="theory")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_section")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"*Вопрос:*\n{card.text}\n\n*Ответ:*\n{card.correct_answer}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

def show_theory(update: Update, context: CallbackContext, card: Question) -> None:
    """Показывает теорию по карточке"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("◀️ Назад к вопросу", callback_data="back_to_card")],
        [InlineKeyboardButton("◀️ Назад к разделу", callback_data="back_to_section")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"*Теория:*\n\n{card.theory}\n\n*Краткое содержание:*\n{card.theory_summary}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    data = query.data
    
    if data == "java_core":
        show_java_core_menu(update, context)
    elif data == "spring":
        show_spring_menu(update, context)
    elif data == "database":
        show_database_menu(update, context)
    elif data == "docker_k8s":
        show_docker_k8s_menu(update, context)
    elif data == "algorithms":
        show_algorithms_menu(update, context)
    elif data == "back":
        # Возвращаемся в главное меню
        start(update, context)
    elif data == "back_to_main":
        start(update, context)
    elif data == "back_to_section":
        # Определяем текущий раздел из контекста
        current_section = context.user_data.get('current_section', 'main')
        if current_section == 'java_core':
            show_java_core_menu(update, context)
        elif current_section == 'spring':
            show_spring_menu(update, context)
        elif current_section == 'database':
            show_database_menu(update, context)
        elif current_section == 'docker_k8s':
            show_docker_k8s_menu(update, context)
        elif current_section == 'algorithms':
            show_algorithms_menu(update, context)
    elif data == "back_to_card":
        # Возвращаемся к текущей карточке
        current_card = context.user_data.get('current_card')
        if current_card:
            show_card(update, context, current_card)
    elif data == "theory":
        # Показываем теорию для текущей карточки
        current_card = context.user_data.get('current_card')
        if current_card:
            show_theory(update, context, current_card)
    elif data.startswith("java_topic_"):
        # Обработка тем Java Core
        index = int(data.split("_")[-1])
        show_java_topic(update, context, index)
    elif data.startswith("spring_topic_"):
        # Обработка тем Spring
        index = int(data.split("_")[-1])
        show_spring_topic(update, context, index)
    elif data.startswith("database_topic_"):
        # Обработка тем Database
        index = int(data.split("_")[-1])
        show_database_topic(update, context, index)
    elif data.startswith("docker_k8s_topic_"):
        # Обработка тем Docker & Kubernetes
        index = int(data.split("_")[-1])
        show_docker_k8s_topic(update, context, index)
    elif data.startswith("algo_"):
        # Обработка карточек Algorithms
        index = int(data.split("_")[1])
        card = ALGORITHMS_CARDS[index]
        context.user_data['current_card'] = card
        context.user_data['current_section'] = 'algorithms'
        show_card(update, context, card)

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

def show_database_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по базам данных"""
    card = DATABASE_CARDS[int(topic_index)]
    message = f"*{card.text}*\n\n"
    message += f"{card.theory}\n\n"
    message += f"*Практические примеры:*\n{card.explanation}"
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='database')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_docker_k8s_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Docker и Kubernetes"""
    card = DOCKER_K8S_CARDS[int(topic_index)]
    message = f"*{card.text}*\n\n"
    message += f"{card.theory}\n\n"
    message += f"*Практические примеры:*\n{card.explanation}"
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='docker_k8s')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_algorithms_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по алгоритмам"""
    card = ALGORITHMS_CARDS[int(topic_index)]
    message = f"*Вопрос:*\n{card['question']}\n\n"
    message += f"*Ответ:*\n{card['answer']}"
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='algorithms')]]
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
        user_states[user_id] = {
            'java_core': set(),
            'spring': set(),
            'database': set(),
            'docker_k8s': set()
        }
    
    java_core_learned = len(user_states[user_id]['java_core'])
    spring_learned = len(user_states[user_id]['spring'])
    database_learned = len(user_states[user_id]['database'])
    docker_k8s_learned = len(user_states[user_id]['docker_k8s'])
    
    message = f"*Ваша статистика:*\n\n"
    message += f"Java Core: {java_core_learned}/{len(JAVA_CORE_CARDS)} тем\n"
    message += f"Spring: {spring_learned}/{len(SPRING_CARDS)} тем\n"
    message += f"Базы данных: {database_learned}/{len(DATABASE_CARDS)} тем\n"
    message += f"Docker & Kubernetes: {docker_k8s_learned}/{len(DOCKER_K8S_CARDS)} тем"
    
    keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
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