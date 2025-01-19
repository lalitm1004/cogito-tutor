export interface Flashcard {
    answer: string;
    question: string;
    subtopic: string;
}

export interface Flashcards {
    topic: string;
    flashcard_pairs: Flashcard[];
}

export interface QuizQuestion {
    answer: string;
    option_A: string;
    option_B: string;
    option_C: string;
    option_D: string;
    question: string;
    subtopic: string;
    explanation: string;
}

export interface Quiz {
    topic: string;
    difficulty: string;
    quiz_questions: QuizQuestion[];
}

export interface DailyContent {
    flashcards: Flashcards;
    quiz: Quiz;
}
