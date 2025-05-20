from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    text: str
    options: List[str]
    correct_answer: str
    explanation: str
    points: int
    theory: str  # Полное теоретическое объяснение
    theory_summary: str  # Краткое резюме теории 