import time
from pathlib import Path
from config import Config
from question_data import QuestionData
from input_reader import InputReader
from file_writer import FileWriter
from statistics import Statistics

class Engine:
    def __init__(self):

        Path(Config.yaml_dir).mkdir(parents=True, exist_ok=True)
        Path(Config.answers_dir).mkdir(parents=True, exist_ok=True)

        self.question_collection = QuestionData()
        self.input_reader = InputReader()
        self.user_name = self.input_reader.read(welcome_message="Enter your name: ")
        self.current_time = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.user_name}_{self.current_time}.txt"
        self.writer = FileWriter("w", filename)
        self.statistics = Statistics(self.writer)

    def run(self):
        print(f"Welcome, {self.user_name}!  Starting the quiz...")
        self.writer.write(f"Quiz started by {self.user_name} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        total_questions = len(self.question_collection.collection)

        for i, question in enumerate(self.question_collection.collection):
            print(f"\nQuestion {i+1}/{total_questions}: {question}")
            self.writer.write(f"\nQuestion {i+1}/{total_questions}: {question}")

            answers = question.display_answers()
            for answer in answers:
                print(answer)
                self.writer.write(answer)

            user_answer = self.get_answer_by_char(question)
            correct_answer = question.question_correct_answer

            self.check(user_answer, correct_answer)

        self.statistics.print_report(total_questions)
        print("Quiz finished.  See report in answers directory.")

    def check(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            print("Correct!")
            self.writer.write("Correct!")
            self.statistics.correct_answer()
        else:
            print(f"Incorrect. The correct answer was {correct_answer}.")
            self.writer.write(f"Incorrect. The correct answer was {correct_answer}.")
            self.statistics.incorrect_answer()

    def get_answer_by_char(self, question):
        validator = lambda x: len(x) > 0 and x[0].upper() in question.question_answers
        error_message = "Invalid input. Please enter a letter corresponding to one of the answers."
        user_answer = self.input_reader.read(
            welcome_message="Enter your answer (A, B, C, etc.): ",
            validator=validator,
            error_message=error_message,
            process=lambda x: x[0].upper()
        )
        return user_answer