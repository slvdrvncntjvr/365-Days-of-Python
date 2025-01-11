import json

class QuestionBank:
    def __init__(self, json_file='questions.json'):
        with open (json_file, 'r') as file:
            self.questions = json.load(file)
        self.current_index = 0

    def get_current_question(self):
        return self.questions[self.current_index]

    def next_question(self):
        self.current_index += 1
        return self.current_index < len(self.questions)

        
