from config import Config
import os

class FileWriter:
    def __init__(self, mode, filename):
        self.answers_dir = Config.answers_dir #Виправлено
        self.filename = filename
        self.mode = mode
        self.filepath = self.prepare_filename(filename)

    def write(self, message):
        try:
            with open(self.filepath, self.mode, encoding="utf-8") as f: # Додано encoding
                f.write(message + "\n")
        except Exception as e:
            print(f"Error writing to file {self.filename}: {e}")

    def prepare_filename(self, filename):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.answers_dir, filename)