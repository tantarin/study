from typing import List, Dict, Optional
import random
from models import Question
from kafka_questions import KAFKA_QUESTIONS

class GameState:
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.questions_answered = 0
        self.questions_per_level = 5
        self.points_to_next_level = 100
        self.current_step = 'theory'  # 'theory', 'summary', 'question'
        self.current_question: Optional[Question] = None  # Текущий вопрос

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
            self.current_question = None
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
            self.current_question = None

class GameManager:
    def __init__(self):
        self.questions: Dict[int, List[Question]] = {}
        self.user_states: Dict[int, GameState] = {}
        self._initialize_questions()

    def _initialize_questions(self):
        # Загружаем вопросы из KAFKA_QUESTIONS
        self.questions = KAFKA_QUESTIONS

    def get_user_state(self, user_id: int) -> GameState:
        if user_id not in self.user_states:
            self.user_states[user_id] = GameState()
        return self.user_states[user_id]

    def get_current_question(self, user_id: int) -> Optional[Question]:
        state = self.get_user_state(user_id)
        
        # Если у нас уже есть текущий вопрос, возвращаем его
        if state.current_question is not None:
            return state.current_question
            
        if state.current_level not in self.questions:
            return None
        
        available_questions = self.questions[state.current_level]
        if not available_questions:
            return None
            
        # Выбираем новый вопрос и сохраняем его
        state.current_question = random.choice(available_questions)
        return state.current_question

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