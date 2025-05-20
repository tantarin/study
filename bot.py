import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from game_logic import GameManager
from kafka_questions import KAFKA_QUESTIONS

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
game_manager.questions = KAFKA_QUESTIONS

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
    """Показывает текущий вопрос пользователю"""
    question = game_manager.get_current_question(user_id)
    if not question:
        if update.callback_query:
            update.callback_query.message.reply_text(
                "Поздравляем! Вы прошли все доступные уровни! 🎉\n"
                "Новые уровни будут добавлены в ближайшее время."
            )
        else:
            update.message.reply_text(
                "Поздравляем! Вы прошли все доступные уровни! 🎉\n"
                "Новые уровни будут добавлены в ближайшее время."
            )
        return

    keyboard = []
    for option in question.options:
        keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{option}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    progress = game_manager.get_level_progress(user_id)
    message_text = (
        f"Уровень {progress['current_level']}\n"
        f"Очки: {progress['score']}\n"
        f"Вопрос {progress['questions_answered'] + 1} из {progress['questions_per_level']}\n\n"
        f"❓ {question.text}"
    )
    
    if update.callback_query:
        update.callback_query.message.reply_text(message_text, reply_markup=reply_markup)
    else:
        update.message.reply_text(message_text, reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    if not query:
        return
        
    try:
        query.answer()
    except Exception as e:
        logger.error(f"Error answering callback query: {e}")
        
    user_id = query.from_user.id
    
    if query.data == 'start_learning':
        query.message.reply_text(
            "🎮 Отлично! Давайте начнем обучение.\n\n"
            "В игре вы будете проходить уровни, отвечая на вопросы о Kafka.\n"
            "За правильные ответы вы получаете очки и открываете новые уровни.\n\n"
            "Готовы начать?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Да, начинаем!", callback_data='level_1')]
            ])
        )
    elif query.data == 'rules':
        query.message.reply_text(
            "📖 Правила игры:\n\n"
            "1. Игра состоит из нескольких уровней\n"
            "2. На каждом уровне вам будут задаваться вопросы о Kafka\n"
            "3. За правильный ответ вы получаете очки\n"
            "4. Для перехода на следующий уровень нужно набрать определенное количество очков\n"
            "5. В конце каждого уровня вы получаете краткое объяснение правильного ответа\n\n"
            "Удачи в обучении! 🚀"
        )
    elif query.data == 'stats':
        state = game_manager.get_user_state(user_id)
        progress = game_manager.get_level_progress(user_id)
        query.message.reply_text(
            f"📊 Ваша статистика:\n\n"
            f"Текущий уровень: {progress['current_level']}\n"
            f"Всего очков: {progress['score']}\n"
            f"Отвечено вопросов: {progress['questions_answered']}\n"
            f"Очков до следующего уровня: {progress['points_to_next_level'] - progress['score']}"
        )
    elif query.data == 'level_1':
        show_question(update, context, user_id)
    elif query.data.startswith('answer_'):
        answer = query.data[7:]  # Убираем префикс 'answer_'
        question = game_manager.get_current_question(user_id)
        
        if game_manager.check_answer(user_id, question, answer):
            query.message.reply_text(
                f"✅ Правильно! +{question.points} очков\n\n"
                f"📝 Объяснение: {question.explanation}"
            )
        else:
            query.message.reply_text(
                f"❌ Неправильно! Правильный ответ: {question.correct_answer}\n\n"
                f"📝 Объяснение: {question.explanation}"
            )
        
        state = game_manager.get_user_state(user_id)
        if state.is_level_complete():
            if state.can_advance_level():
                state.advance_level()
                query.message.reply_text(
                    f"🎉 Поздравляем! Вы перешли на уровень {state.current_level}!\n\n"
                    "Готовы к новым вопросам?",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Продолжить", callback_data='level_1')]
                    ])
                )
            else:
                query.message.reply_text(
                    f"🏁 Уровень завершен!\n"
                    f"Для перехода на следующий уровень нужно набрать {state.points_to_next_level} очков.\n"
                    f"Текущий счет: {state.score}\n\n"
                    "Продолжайте отвечать на вопросы!",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Следующий вопрос", callback_data='level_1')]
                    ])
                )
        else:
            show_question(update, context, user_id)

def main():
    """Запуск бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Добавляем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 