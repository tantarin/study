from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu() -> InlineKeyboardMarkup:
    """Получить главное меню"""
    keyboard = [
        [InlineKeyboardButton("Java Core", callback_data='java_core')],
        [InlineKeyboardButton("Spring Framework", callback_data='spring')],
        [InlineKeyboardButton("Базы данных", callback_data='database')],
        [InlineKeyboardButton("Docker & Kubernetes", callback_data='docker_k8s')],
        [InlineKeyboardButton("Статистика", callback_data='stats')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_topic_menu(cards, prefix: str) -> InlineKeyboardMarkup:
    """Получить меню тем для раздела"""
    keyboard = []
    for i, card in enumerate(cards):
        keyboard.append([InlineKeyboardButton(
            card.text,
            callback_data=f'{prefix}_topic_{i}'
        )])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    return InlineKeyboardMarkup(keyboard)

def get_back_button(callback_data: str) -> InlineKeyboardMarkup:
    """Получить кнопку 'Назад'"""
    keyboard = [[InlineKeyboardButton("Назад к темам", callback_data=callback_data)]]
    return InlineKeyboardMarkup(keyboard) 