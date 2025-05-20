from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Question:
    """Модель карточки с вопросом"""
    text: str  # Текст вопроса/темы
    theory: str  # Подробная теория
    theory_summary: str  # Краткое описание теории
    explanation: str  # Объяснение с примерами
    points: int = 0  # Количество набранных очков
    correct_answer: Optional[str] = None  # Правильный ответ (если есть)
    options: Optional[List[str]] = None  # Варианты ответов (если есть) 