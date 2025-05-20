from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Question:
    text: str
    options: List[str]
    correct_answer: str
    explanation: str
    points: int
    theory: str  # Полное теоретическое объяснение
    theory_summary: str  # Краткое резюме теории

class GameState:
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.questions_answered = 0
        self.questions_per_level = 5
        self.points_to_next_level = 100
        self.current_step = 'theory'  # 'theory', 'summary', 'question'

    def is_level_complete(self) -> bool:
        return self.questions_answered >= self.questions_per_level

    def add_points(self, points: int):
        self.score += points
        self.questions_answered += 1

    def can_advance_level(self) -> bool:
        return self.score >= self.points_to_next_level * self.current_level

    def advance_level(self):
        if self.can_advance_level():
            self.current_level += 1
            self.questions_answered = 0
            self.current_step = 'theory'
            return True
        return False

    def next_step(self):
        if self.current_step == 'theory':
            self.current_step = 'summary'
        elif self.current_step == 'summary':
            self.current_step = 'question'
        else:
            self.current_step = 'theory'
            self.questions_answered += 1

class GameManager:
    def __init__(self):
        self.questions: Dict[int, List[Question]] = {}
        self.user_states: Dict[int, GameState] = {}
        self._initialize_questions()

    def _initialize_questions(self):
        # TODO: Загружать вопросы из базы данных или файла
        self.questions[1] = [
            Question(
                text="Что такое Apache Kafka?",
                options=[
                    "Система управления базами данных",
                    "Распределенная система обмена сообщениями",
                    "Веб-сервер",
                    "Система кэширования"
                ],
                correct_answer="Распределенная система обмена сообщениями",
                explanation="Apache Kafka - это распределенная система обмена сообщениями, которая позволяет обрабатывать большие объемы данных в реальном времени.",
                points=20,
                theory="Apache Kafka - это распределенная система обмена сообщениями, разработанная LinkedIn и переданная в Apache Software Foundation. Она предназначена для обработки больших объемов данных в реальном времени. Kafka использует модель публикации-подписки, где производители публикуют сообщения в топики, а потребители подписываются на эти топики для получения сообщений. Система обеспечивает высокую пропускную способность, отказоустойчивость и масштабируемость.",
                theory_summary="Kafka - это система обмена сообщениями, где производители публикуют данные в топики, а потребители читают из них. Она обеспечивает высокую производительность и надежность."
            ),
            # Добавьте больше вопросов здесь
        ]

    def get_user_state(self, user_id: int) -> GameState:
        if user_id not in self.user_states:
            self.user_states[user_id] = GameState()
        return self.user_states[user_id]

    def get_current_question(self, user_id: int) -> Optional[Question]:
        state = self.get_user_state(user_id)
        if state.current_level not in self.questions:
            return None
        
        available_questions = self.questions[state.current_level]
        if not available_questions:
            return None
            
        return random.choice(available_questions)

    def check_answer(self, user_id: int, question: Question, answer: str) -> bool:
        is_correct = answer == question.correct_answer
        if is_correct:
            self.get_user_state(user_id).add_points(question.points)
        return is_correct

    def get_level_progress(self, user_id: int) -> Dict:
        state = self.get_user_state(user_id)
        return {
            "current_level": state.current_level,
            "score": state.score,
            "questions_answered": state.questions_answered,
            "questions_per_level": state.questions_per_level,
            "points_to_next_level": state.points_to_next_level * state.current_level,
            "current_step": state.current_step
        } 