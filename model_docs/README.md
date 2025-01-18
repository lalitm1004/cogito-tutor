
## Requirements
Install dependencies:

```
pip install openai pydantic
```

Set up a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```
----------
## Methods

### 1. **Generate Flashcards**

-   **Method**: `Completions.return_flashcards(topic: str) -> Dict`
-   **Purpose**: generates a set of flashcards for a specified topic
-   **Parameters**:
    -   `topic`: subject for which flashcards should be generated
-   **Example**:
```
from generation_methods.completions import Completions
flashcards = Completions.return_flashcards("Poetic Devices")
```
- **Format**: 
```
FlashCard: {
	subtopic: str
	question: str
	answer: str
}
```
```
FlashCardResponseFormat: {
	topic: str
	flashcard_pairs: List[FlashCard]
}
```
### 2. **Generate Quiz**

-   **Method**: `Completions.return_quiz(topic: str, difficulty: int) -> Dict`
-   **Description**: generates quiz questions for a topic with a specific difficulty level
-   **Parameters**:
    -   `topic`: the topic for the quiz
    -   `difficulty`: the difficulty of the quiz: Easy(1), Medium(2), or Hard(3)
-   **Example**:
```
from generation_methods.completions import Completions

quiz = Completions.return_quiz("Java Basics", difficulty = 2)
```
- **Format**: 
```
QuizQuestion: {
	subtopic: str
	question: str
	option_A: str
	option_B: str
	option_C: str
	option_D: str
	answer: AnswerOption
	explanation: str
}
```
```
QuizResponseFormat: {
	topic: str
	difficulty: QuizDifficulty
	quiz_questions: List[QuizQuestion]
}
```
### 3. **Generate Weekly Schedule**

-   **Method**: `Completions.return_week_schedule(topic: str, desc: str) -> Dict`
-   **Description**: generates a weeklong learning schedule, breaking down subtopics for each day
-   **Parameters**:
    -   `topic`: the overall subject for the weekly schedule to plan out
	-   `desc`: the user provided description ideally including the syllabus, strong and weak topics
-   **Example**:
```
week_schedule = Completions.return_week_schedule("Machine Learning", "(A brief user provided description)")
```
- **Format**: 
```
DaySchedule: {
	subtopic: str
	subtopic_description: str
	progress_revision_topic: str
}
```
```
ScheduleResponseFormat: {
	topic: str
	day_1: DaySchedule
	day_2: DaySchedule
	day_3: DaySchedule
	day_4: DaySchedule
	day_5: DaySchedule
	day_6: DaySchedule
	day_7: DaySchedule
}
```

### 4. **Generate Weekly Materials**

-   **Method**: `Completions.return_week_material(schedule: Dict) -> Dict`
-   **Description**: generates a full set of learning materials broken down over a week, including flashcards and quizzes
-   **Parameters**:
    -   `schedule`: the schedule dictionary (generated using `return_week_schedule()`)
-   **Example**:
```
week_schedule = Completions.return_week_schedule("Game Theory")
week_material = Completions.return_week_material(week_schedule)
```
- **Format**: 
```
DayMaterial (not a pydantic BaseModel): {
	subtopic: str
	subtopic_description: str
	flashcard_deck: FlashCardResponseFormat
	progress_revision_topic: str
	revision_quiz: QuizResponseFormat
}
```
```
MaterialResponseFormat (not a pydantic BaseModel):
	topic: str
	day_1: DayMaterial
	day_2: DayMaterial
	day_3: DayMaterial
	day_4: DayMaterial
	day_5: DayMaterial
	day_6: DayMaterial
	day_7: DayMaterial
```
----------

## Classes and Methods

-   **Completions Class**: contains the methods for generating study materials
    -   `return_flashcards(topic: str)`: generates flashcards
    -   `return_quiz(topic: str, difficulty: int)`: generates quiz questions
    -   `return_week_schedule(topic: str)`: generates a 7-day study schedule
    -   `return_week_material(schedule: Dict)`: generates full study materials for the week
    
-   **QuizDifficulty Enum**: defines quiz difficulty levels, corresponding to an integer in method parameters:
    -   Easy (1)
    -   Medium (2)
    -   Hard (3)
