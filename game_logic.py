from typing import List, Dict, Optional
import random
from models import Question
from kafka_cards import KAFKA_CARDS

class GameState:
    def __init__(self):
        self.viewed_card_indices = set()  # Множество индексов просмотренных карточек
        self.current_card: Optional[Question] = None  # Текущая карточка

    def next_card(self):
        if self.current_card:
            # Находим индекс текущей карточки
            for i, card in enumerate(KAFKA_CARDS):
                if card == self.current_card:
                    self.viewed_card_indices.add(i)
                    break
        self.current_card = None

class GameManager:
    def __init__(self):
        self.cards = KAFKA_CARDS
        self.user_states: Dict[int, GameState] = {}

    def get_user_state(self, user_id: int) -> GameState:
        if user_id not in self.user_states:
            self.user_states[user_id] = GameState()
        return self.user_states[user_id]

    def get_current_question(self, user_id: int) -> Optional[Question]:
        state = self.get_user_state(user_id)
        
        # Если просмотрены все карточки, возвращаем None
        if len(state.viewed_card_indices) >= len(self.cards):
            return None
            
        # Выбираем случайную непросмотренную карточку
        available_indices = [i for i in range(len(self.cards)) if i not in state.viewed_card_indices]
        if not available_indices:
            return None
            
        random_index = random.choice(available_indices)
        state.current_card = self.cards[random_index]
        return state.current_card

    def get_level_progress(self, user_id: int) -> Dict:
        state = self.get_user_state(user_id)
        return {
            "cards_viewed": len(state.viewed_card_indices),
            "total_cards": len(self.cards)
        } 