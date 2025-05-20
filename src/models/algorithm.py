from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AlgorithmExample:
    """Модель примера для алгоритма"""
    input_data: str
    output_data: str
    explanation: str

@dataclass
class Algorithm:
    """Модель алгоритмической задачи"""
    title: str  # Название алгоритма
    description: str  # Описание алгоритма
    complexity: str  # Сложность алгоритма (O-нотация)
    theory: str  # Теоретическое объяснение
    visualization_url: str  # Ссылка на визуализацию (например, на visualgo.net)
    java_code: str  # Реализация на Java
    python_code: Optional[str] = None  # Реализация на Python (опционально)
    leetcode_problems: List[str] = None  # Список связанных задач на LeetCode
    examples: List[AlgorithmExample] = None  # Примеры работы алгоритма
    category: str = "general"  # Категория алгоритма (сортировка, поиск и т.д.)
    difficulty: str = "medium"  # Сложность: easy, medium, hard
    
    def __post_init__(self):
        if self.leetcode_problems is None:
            self.leetcode_problems = []
        if self.examples is None:
            self.examples = [] 