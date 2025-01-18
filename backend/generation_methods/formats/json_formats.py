from typing import List, Dict
from pydantic import BaseModel
from .enums import QuizDifficulty, AnswerOption

class ItemFormats:
    class FlashCard(BaseModel):
        subtopic: str
        question: str
        answer: str
    
    class QuizQuestion(BaseModel):
        subtopic: str
        question: str
        option_A: str
        option_B: str
        option_C: str
        option_D: str
        answer: AnswerOption
        explanation: str

    class DaySchedule(BaseModel):
        subtopic: str
        subtopic_description: str
        progress_revision_topic: str

class ResponseFormats:
    class FlashCardResponseFormat(BaseModel):
        topic: str
        flashcard_pairs: List[ItemFormats.FlashCard]

    class QuizResponseFormat(BaseModel):
        topic: str
        difficulty: QuizDifficulty
        quiz_questions: List[ItemFormats.QuizQuestion]

    class ScheduleResponseFormat(BaseModel):
        topic: str
        day_1: ItemFormats.DaySchedule
        day_2: ItemFormats.DaySchedule
        day_3: ItemFormats.DaySchedule
        day_4: ItemFormats.DaySchedule
        day_5: ItemFormats.DaySchedule
        day_6: ItemFormats.DaySchedule
        day_7: ItemFormats.DaySchedule