import json
from typing import Dict
from .utils.config import Config
from .model_prompts.prompts import SystemPrompts
from .formats.json_formats import ResponseFormats
from .formats.enums import QuizDifficulty

class CompletionFormat:
    @staticmethod
    def return_completion(topic: str, system_prompt: str, user_prompt: str, response_format: ResponseFormats) -> Dict:
        try:
            completion = Config.OPENAI_CLIENT.beta.chat.completions.parse(
                model = Config.MODEL_NAME,
                messages = [{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}],
                response_format = response_format)
            
            event = completion.choices[0].message.content
            event = json.loads(event)
            
            return event
        except Exception as e:
            print(f"Error in return_completion: {e}")
            return {}

class Completions:
    @staticmethod
    def return_flashcards(topic: str) -> Dict:
        try:
            system_prompt = SystemPrompts.flashcard_system_prompt
            user_prompt = f"Please generate flashcards for the topic {topic}."
            response_format = ResponseFormats.FlashCardResponseFormat
            iter_name = "flashcard_pairs"
            num_iter = Config.NUM_FLASHCARDS

            event = CompletionFormat.return_completion(topic = topic, 
                                                       system_prompt = system_prompt, 
                                                       user_prompt = user_prompt, 
                                                       response_format = response_format)

            if not event or len(event.get(iter_name, [])) < num_iter:
                event = Completions.return_flashcards(topic)

            event[iter_name] = event[iter_name][:num_iter]

            return event
        except Exception as e:
            print(f"Error in return_flashcards: {e}")
            return {}

    @staticmethod
    def return_quiz(topic: str, difficulty: int) -> Dict:
        try:
            difficulty_mapping = {
            1: QuizDifficulty.Easy,
            2: QuizDifficulty.Medium,
            3: QuizDifficulty.Hard
            }

            difficulty_enum = difficulty_mapping.get(difficulty)

            if not difficulty_enum:
                raise ValueError("Invalid difficulty level. Must be 1 (Easy), 2 (Medium), or 3 (Hard).")

            system_prompt = SystemPrompts.quiz_system_prompt
            user_prompt = f"Please generate quiz questions for the topic {topic} with a given difficulty of {difficulty_enum}."
            response_format = ResponseFormats.QuizResponseFormat
            iter_name = "quiz_questions"
            num_iter = Config.NUM_QUIZ_QUESTIONS

            event = CompletionFormat.return_completion(topic = topic, 
                                                       system_prompt = system_prompt, 
                                                       user_prompt = user_prompt, 
                                                       response_format = response_format)

            if not event or len(event.get(iter_name, [])) < num_iter:
                event = Completions.return_quiz(topic, difficulty)

            event[iter_name] = event[iter_name][:num_iter]

            return event
        except Exception as e:
            print(f"Error in return_quiz: {e}")
            return {}

    @staticmethod
    def return_week_schedule(topic: str, desc: str) -> Dict:
        try:
            system_prompt = SystemPrompts.schedule_system_prompt
            user_prompt = f"Please generate a schedule for the overall subject {topic}. Here is a brief description of the syllabus and the user's strengths and weaknesses: {desc}"
            response_format = ResponseFormats.ScheduleResponseFormat

            basic_schedule = CompletionFormat.return_completion(topic = topic, 
                                                                  system_prompt = system_prompt, 
                                                                  user_prompt = user_prompt, 
                                                                  response_format = response_format)

            return basic_schedule
        except Exception as e:
            print(f"Error in return_week_schedule: {e}")
            return {}

    @staticmethod
    def return_week_material(schedule: Dict) -> Dict:
        try:
            basic_schedule = schedule
            complete_material = {"topic": basic_schedule.get("topic", "")}

            for day in range(1, 8):
                current_subtopic = basic_schedule.get(f"day_{day}", {}).get("subtopic", "")
                subtopic_description = basic_schedule.get(f"day_{day}", {}).get("subtopic_description", "")
                revision_topic = basic_schedule.get(f"day_{day}", {}).get("progress_revision_topic", "")
                daily_flashcards = Completions.return_flashcards(current_subtopic)

                if day < 3:
                    quiz_difficulty = 1
                elif day >= 3 and day < 6:
                    quiz_difficulty = 2
                else:
                    quiz_difficulty = 3

                daily_quiz = Completions.return_quiz(topic = revision_topic, 
                                                     difficulty = quiz_difficulty)

                day_materials = {"subtopic": current_subtopic,
                                 "subtopic_description": subtopic_description,
                                 "flashcard_deck": daily_flashcards,
                                 "progress_revision_topic": revision_topic,
                                 "revision_quiz": daily_quiz}
                
                complete_material[f"day_{day}"] = day_materials

            return complete_material
        except Exception as e:
            print(f"Error in return_week_material: {e}")
            return {}
