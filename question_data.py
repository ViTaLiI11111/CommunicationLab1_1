from config import Config
import os
import yaml
from question import Question

class QuestionData:
    def __init__(self):
        self.collection = []
        self.yaml_dir = Config.yaml_dir
        self.in_ext = Config.in_ext
        self.threads = []
        self.load_data()

    def to_yaml(self):
        import yaml
        return yaml.dump([q.to_h() for q in self.collection])

    def save_to_yaml(self, filename="questions.yml"):
        with open(filename, "w") as f:
            f.write(self.to_yaml())

    def to_json(self):
        import json
        return json.dumps([q.to_h() for q in self.collection])

    def save_to_json(self, filename="questions.json"):
        with open(filename, "w") as f:
            f.write(self.to_json())

    def prepare_filename(self, filename):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    def each_file(self, block):
        import glob
        path = self.prepare_filename(self.yaml_dir)
        files = glob.glob(os.path.join(path, f"*.{self.in_ext}"))
        for filename in files:
            block(filename)

    def in_thread(self, block):
        import threading
        thread = threading.Thread(target=block)
        self.threads.append(thread)
        thread.start()

    def load_data(self):
        def load(filename):
            try:
                self.load_from(filename)
            except Exception as e:
                print(f"Error loading from {filename}: {e}")

        self.each_file(lambda filename: self.in_thread(lambda: load(filename)))

        for thread in self.threads:
            thread.join()

        self.threads = []

    def load_from(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "question" in item and "answers" in item:
                            question = Question(item["question"], item["answers"])
                            self.collection.append(question)
                        else:
                            print(f"Warning: Invalid data format in {filename}.  Skipping entry.")
                else:
                    print(f"Warning: Invalid data format in {filename}.  Expected a list.")


        except FileNotFoundError:
            print(f"File not found: {filename}")
        except yaml.YAMLError as e:
            print(f"YAML error in {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while loading {filename}: {e}")