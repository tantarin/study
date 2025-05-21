import os
import logging
import re
import html
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from src.models import Question
from src.cards import (
    JAVA_CORE_CARDS,
    SPRING_CARDS,
    DATABASE_CARDS,
    DOCKER_K8S_CARDS,
    ALGORITHMS
)
from src.cards.algorithms import ALGORITHMS
from src.cards.system_design import SYSTEM_DESIGN_CARDS
import tempfile
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

CATEGORIES = {
    "algorithms": {
        "name": "🔄 Алгоритмы",
        "cards": ALGORITHMS
    },
    "system_design": {
        "name": "🏗 System Design",
        "cards": SYSTEM_DESIGN_CARDS
    }
}

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        update.effective_message.reply_text(
            "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз или начните сначала с помощью команды /start"
        )

def create_full_theory_markdown() -> str:
    """Создает Markdown файл со всей теорией из всех разделов"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
        # Заголовок документа
        tmp_file.write('# Полная теория по всем разделам\n\n')
        
        # Java Core
        tmp_file.write('# Java Core\n\n')
        for card in JAVA_CORE_CARDS:
            tmp_file.write(f'## {card.text}\n\n')
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            tmp_file.write('---\n\n')
        
        # Spring Framework
        tmp_file.write('# Spring Framework\n\n')
        for card in SPRING_CARDS:
            tmp_file.write(f'## {card.text}\n\n')
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            tmp_file.write('---\n\n')
        
        # Базы данных
        tmp_file.write('# Базы данных\n\n')
        for card in DATABASE_CARDS:
            tmp_file.write(f'## {card.text}\n\n')
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            tmp_file.write('---\n\n')
        
        # Docker и Kubernetes
        tmp_file.write('# Docker и Kubernetes\n\n')
        for card in DOCKER_K8S_CARDS:
            tmp_file.write(f'## {card.text}\n\n')
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            tmp_file.write('---\n\n')
        
        # Алгоритмы
        tmp_file.write('# Алгоритмы\n\n')
        for algo in ALGORITHMS:
            tmp_file.write(f'## {algo.title}\n\n')
            tmp_file.write('### Описание\n')
            tmp_file.write(f'{algo.description}\n\n')
            tmp_file.write('### Сложность\n')
            tmp_file.write(f'{algo.complexity}\n\n')
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{algo.theory}\n\n')
            if algo.examples:
                tmp_file.write('### Примеры\n')
                for i, example in enumerate(algo.examples, 1):
                    tmp_file.write(f'#### Пример {i}\n')
                    tmp_file.write(f'- Вход: `{example.input_data}`\n')
                    tmp_file.write(f'- Выход: `{example.output_data}`\n')
                    tmp_file.write(f'- Объяснение: {example.explanation}\n\n')
            tmp_file.write('### Реализация на Java\n```java\n')
            tmp_file.write(f'{algo.java_code}\n```\n\n')
            if algo.python_code:
                tmp_file.write('### Реализация на Python\n```python\n')
                tmp_file.write(f'{algo.python_code}\n```\n\n')
            if algo.leetcode_problems:
                tmp_file.write('### Задачи на LeetCode\n')
                for problem in algo.leetcode_problems:
                    tmp_file.write(f'- {problem}\n')
                tmp_file.write('\n')
            tmp_file.write('---\n\n')
        
        return tmp_file.name

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Java Core", callback_data='java_core')],
        [InlineKeyboardButton("Spring Framework", callback_data='spring')],
        [InlineKeyboardButton("Базы данных", callback_data='database')],
        [InlineKeyboardButton("Docker & Kubernetes", callback_data='docker_k8s')],
        [InlineKeyboardButton("Алгоритмы", callback_data='algorithms')],
        [InlineKeyboardButton("🏗 System Design", callback_data='system_design')],
        [InlineKeyboardButton("📝 Скачать всю теорию", callback_data='md_full')]
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

def create_database_markdown(cards) -> str:
    """Создает Markdown файл с теорией по базам данных"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
        tmp_file.write('# Теория по базам данных\n\n')
        
        for card in cards:
            # Заголовок темы
            tmp_file.write(f'## {card.text}\n\n')
            
            # Теория
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            
            # Примеры
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            
            # Разделитель между темами
            tmp_file.write('---\n\n')
        
        return tmp_file.name

def show_database_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем по базам данных"""
    keyboard = []
    for i, card in enumerate(DATABASE_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'database_topic_{i}'
        )])
    
    # Добавляем кнопку для скачивания теории
    keyboard.append([InlineKeyboardButton("📝 Скачать теорию в Markdown", callback_data="md_database")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по базам данных:",
        reply_markup=reply_markup
    )

def create_docker_k8s_markdown(cards) -> str:
    """Создает Markdown файл с теорией по Docker и Kubernetes"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
        tmp_file.write('# Теория по Docker и Kubernetes\n\n')
        
        for card in cards:
            # Заголовок темы
            tmp_file.write(f'## {card.text}\n\n')
            
            # Теория
            tmp_file.write('### Теория\n')
            tmp_file.write(f'{card.theory}\n\n')
            
            # Примеры
            tmp_file.write('### Практические примеры\n')
            tmp_file.write(f'{card.explanation}\n\n')
            
            # Разделитель между темами
            tmp_file.write('---\n\n')
        
        return tmp_file.name

def show_docker_k8s_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем по Docker и Kubernetes"""
    keyboard = []
    for i, card in enumerate(DOCKER_K8S_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'docker_k8s_topic_{i}'
        )])
    
    # Добавляем кнопку для скачивания теории
    keyboard.append([InlineKeyboardButton("📝 Скачать теорию в Markdown", callback_data="md_docker_k8s")])
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
    
    # Группируем алгоритмы по категориям
    categories = {}
    for algo in ALGORITHMS:
        if algo.category not in categories:
            categories[algo.category] = []
        categories[algo.category].append(algo)
    
    keyboard = []
    # Добавляем кнопки по категориям
    for category, algos in categories.items():
        keyboard.append([InlineKeyboardButton(
            f"📚 {category.capitalize()} ({len(algos)})",
            callback_data=f"cat_{category}"
        )])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите категорию алгоритмов:",
        reply_markup=reply_markup
    )

def escape_markdown(text: str) -> str:
    """Экранирует специальные символы Markdown"""
    # Список всех специальных символов Markdown
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    
    # Сначала экранируем обратный слеш
    text = text.replace('\\', '\\\\')
    
    # Затем экранируем все остальные специальные символы
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def create_theory_markdown(algorithms, category: str) -> str:
    """Создает Markdown файл с теорией по категории алгоритмов"""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
        # Записываем заголовок
        tmp_file.write(f'# Теория по разделу: {category.capitalize()}\n\n')
        
        # Добавляем содержание для каждого алгоритма
        for algo in algorithms:
            if algo.category == category:
                # Заголовок алгоритма
                tmp_file.write(f'## {algo.title}\n\n')
                
                # Описание
                tmp_file.write(f'### Описание\n{algo.description}\n\n')
                
                # Сложность
                tmp_file.write(f'### Сложность\n{algo.complexity}\n\n')
                
                # Теория
                tmp_file.write(f'### Теория\n{algo.theory}\n\n')
                
                # Примеры
                if algo.examples:
                    tmp_file.write('### Примеры\n')
                    for i, example in enumerate(algo.examples, 1):
                        tmp_file.write(f'#### Пример {i}\n')
                        tmp_file.write(f'- Вход: `{example.input_data}`\n')
                        tmp_file.write(f'- Выход: `{example.output_data}`\n')
                        tmp_file.write(f'- Объяснение: {example.explanation}\n\n')
                
                # Код на Java
                tmp_file.write('### Реализация на Java\n```java\n')
                tmp_file.write(algo.java_code)
                tmp_file.write('\n```\n\n')
                
                # Код на Python (если есть)
                if algo.python_code:
                    tmp_file.write('### Реализация на Python\n```python\n')
                    tmp_file.write(algo.python_code)
                    tmp_file.write('\n```\n\n')
                
                # Задачи на LeetCode
                if algo.leetcode_problems:
                    tmp_file.write('### Задачи на LeetCode\n')
                    for problem in algo.leetcode_problems:
                        tmp_file.write(f'- {problem}\n')
                    tmp_file.write('\n')
                
                # Визуализация
                tmp_file.write(f'### Визуализация\n{algo.visualization_url}\n\n')
                
                # Разделитель между алгоритмами
                tmp_file.write('---\n\n')
        
        return tmp_file.name

def show_algorithm_category(update: Update, context: CallbackContext, category: str) -> None:
    """Показывает список алгоритмов в категории"""
    query = update.callback_query
    
    keyboard = []
    for i, algo in enumerate(ALGORITHMS):
        if algo.category == category:
            difficulty_emoji = "🟢" if algo.difficulty == "easy" else "🟡" if algo.difficulty == "medium" else "🔴"
            keyboard.append([InlineKeyboardButton(
                f"{difficulty_emoji} {algo.title}",
                callback_data=f"a_{i}"
            )])
    
    # Добавляем кнопку для создания Markdown
    keyboard.append([InlineKeyboardButton("📝 Скачать теорию в Markdown", callback_data=f"md_{category}")])
    keyboard.append([InlineKeyboardButton("◀️ Назад к категориям", callback_data="algorithms")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Алгоритмы в категории {category.capitalize()}:",
        reply_markup=reply_markup
    )

def show_algorithm(update: Update, context: CallbackContext, algo_index: int) -> None:
    """Показывает детальную информацию об алгоритме"""
    query = update.callback_query
    algo = ALGORITHMS[algo_index]
    
    # Формируем текст сообщения с HTML форматированием
    message = f"<b>{html.escape(algo.title)}</b>\n\n"
    message += f"📝 <b>Описание:</b>\n{html.escape(algo.description)}\n\n"
    message += f"⚡️ <b>Сложность:</b>\n{html.escape(algo.complexity)}\n\n"
    message += f"📚 <b>Теория:</b>\n{html.escape(algo.theory)}\n\n"
    message += f"🔗 <b>Визуализация:</b>\n{html.escape(algo.visualization_url)}\n\n"
    
    # Код обрабатываем отдельно
    message += f"💻 <b>Java код:</b>\n<pre>{html.escape(algo.java_code)}</pre>\n\n"
    
    if algo.python_code:
        message += f"🐍 <b>Python код:</b>\n<pre>{html.escape(algo.python_code)}</pre>\n\n"
    
    if algo.examples:
        message += "<b>Примеры:</b>\n"
        for i, example in enumerate(algo.examples, 1):
            message += f"\nПример {i}:\n"
            message += f"Вход: <code>{html.escape(example.input_data)}</code>\n"
            message += f"Выход: <code>{html.escape(example.output_data)}</code>\n"
            message += f"Объяснение: {html.escape(example.explanation)}\n"
    
    if algo.leetcode_problems:
        message += "\n<b>Задачи на LeetCode:</b>\n"
        for problem in algo.leetcode_problems:
            message += f"• {html.escape(problem)}\n"
    
    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton("◀️ Назад к списку", callback_data=f"cat_{algo.category}")],
        [InlineKeyboardButton("◀️ В главное меню", callback_data="back")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение частями из-за ограничений Telegram
    if len(message) > 4096:
        parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for i, part in enumerate(parts):
            if i == 0:
                query.edit_message_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.HTML
                )
            else:
                query.message.reply_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.HTML
                )
    else:
        query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
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

def show_system_design_menu(update: Update, context: CallbackContext) -> None:
    """Показать меню тем System Design"""
    keyboard = []
    for i, card in enumerate(SYSTEM_DESIGN_CARDS):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'system_design_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        text="Выберите тему по System Design:",
        reply_markup=reply_markup
    )

def process_code_blocks(text: str, language: str = None) -> str:
    """Обрабатывает блоки кода в тексте"""
    if not text:
        return ""
        
    # Если язык не указан, пробуем определить его из текста
    if not language:
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            language = code_blocks[0][0] or 'text'
    
    # Разбиваем текст на части по блокам кода
    parts = text.split('```')
    result = []
    
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Обычный текст
            # Экранируем специальные символы Markdown
            result.append(escape_markdown(part))
        else:  # Блок кода
            # Определяем язык и код
            if '\n' in part:
                lang, code = part.split('\n', 1)
            else:
                lang, code = language or 'text', part
                
            # Добавляем код в Markdown формате
            code_lines = code.strip().split('\n')
            formatted_code = '\n'.join(code_lines)
            result.append(f'\n```{lang}\n{formatted_code}\n```\n')
    
    return ''.join(result)

def show_system_design_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по System Design"""
    card = SYSTEM_DESIGN_CARDS[topic_index]
    message = f"*{escape_markdown(card.text)}*\n\n"
    message += process_code_blocks(card.theory)
    message += "\n\n*Практические примеры:*\n"
    message += process_code_blocks(card.explanation)
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='system_design')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Разбиваем сообщение на части, если оно слишком длинное
    if len(message) > 4096:
        parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for i, part in enumerate(parts):
            if i == 0:
                update.callback_query.edit_message_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.callback_query.message.reply_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.MARKDOWN
                )
    else:
        update.callback_query.edit_message_text(
            text=message,
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
    elif data == "system_design":
        show_system_design_menu(update, context)
    elif data.startswith("system_design_topic_"):
        topic_index = int(data.split("_")[-1])
        show_system_design_topic(update, context, topic_index)
    elif data.startswith("cat_"):
        category = data[4:]
        show_algorithm_category(update, context, category)
    elif data.startswith("a_"):
        algo_index = int(data[2:])
        show_algorithm(update, context, algo_index)
    elif data.startswith("md_"):
        category = data[3:]
        if category == "full":
            # Открываем теорию в браузере
            from src.theory_server import open_theory_in_browser
            open_theory_in_browser()
            query.message.reply_text("Теория открыта в вашем браузере! Если страница не открылась автоматически, перейдите по адресу: http://localhost:5000")
            query.answer("Теория открыта в браузере!")
        elif category == "database":
            # Создаем Markdown для баз данных
            md_path = create_database_markdown(DATABASE_CARDS)
            # Отправляем файл
            with open(md_path, 'rb') as md_file:
                query.message.reply_document(
                    document=md_file,
                    filename='theory_database.md',
                    caption='Теория по разделу: Базы данных'
                )
            # Удаляем временный файл
            os.unlink(md_path)
            # Отвечаем на callback
            query.answer("Markdown файл создан и отправлен!")
        elif category == "docker_k8s":
            # Создаем Markdown для Docker и Kubernetes
            md_path = create_docker_k8s_markdown(DOCKER_K8S_CARDS)
            # Отправляем файл
            with open(md_path, 'rb') as md_file:
                query.message.reply_document(
                    document=md_file,
                    filename='theory_docker_k8s.md',
                    caption='Теория по разделу: Docker и Kubernetes'
                )
            # Удаляем временный файл
            os.unlink(md_path)
            # Отвечаем на callback
            query.answer("Markdown файл создан и отправлен!")
        else:
            # Создаем Markdown для алгоритмов
            md_path = create_theory_markdown(ALGORITHMS, category)
            # Отправляем файл
            with open(md_path, 'rb') as md_file:
                query.message.reply_document(
                    document=md_file,
                    filename=f'theory_{category}.md',
                    caption=f'Теория по разделу: {category.capitalize()}'
                )
            # Удаляем временный файл
            os.unlink(md_path)
            # Отвечаем на callback
            query.answer("Markdown файл создан и отправлен!")
    elif data == "back":
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
        elif current_section == 'system_design':
            show_system_design_menu(update, context)
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

def show_java_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Java Core"""
    card = JAVA_CORE_CARDS[int(topic_index)]
    message = f"*{escape_markdown(card.text)}*\n\n"
    message += process_code_blocks(card.theory, 'java')
    message += "\n\n*Практические примеры:*\n"
    message += process_code_blocks(card.explanation, 'java')
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='java_core')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Разбиваем сообщение на части, если оно слишком длинное
    if len(message) > 4096:
        parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for i, part in enumerate(parts):
            if i == 0:
                update.callback_query.edit_message_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.callback_query.message.reply_text(
                    text=part,
                    reply_markup=reply_markup if i == len(parts)-1 else None,
                    parse_mode=ParseMode.MARKDOWN
                )
    else:
        update.callback_query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

def show_spring_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Spring"""
    card = SPRING_CARDS[int(topic_index)]
    message = f"*{escape_markdown(card.text)}*\n\n"
    message += process_code_blocks(card.theory, 'java')
    message += "\n\n*Практические примеры:*\n"
    message += process_code_blocks(card.explanation, 'java')
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='spring')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

def show_database_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по базам данных"""
    card = DATABASE_CARDS[int(topic_index)]
    message = f"*{escape_markdown(card.text)}*\n\n"
    message += process_code_blocks(card.theory, 'sql')
    message += "\n\n*Практические примеры:*\n"
    message += process_code_blocks(card.explanation, 'sql')
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='database')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

def show_docker_k8s_topic(update: Update, context: CallbackContext, topic_index: int) -> None:
    """Показать тему по Docker и Kubernetes"""
    card = DOCKER_K8S_CARDS[int(topic_index)]
    message = f"*{escape_markdown(card.text)}*\n\n"
    message += process_code_blocks(card.theory, 'yaml')
    message += "\n\n*Практические примеры:*\n"
    message += process_code_blocks(card.explanation, 'yaml')
    
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data='docker_k8s')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
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