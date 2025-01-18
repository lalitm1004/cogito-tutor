from enum import Enum

class QuizDifficulty(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class AnswerOption(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
