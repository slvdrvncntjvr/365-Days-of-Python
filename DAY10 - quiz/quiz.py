class QuestionBank:
    def __init__(self):
      #insert questions here
        self.questions = [
            {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
            {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
            {"question": "Who wrote '1984'?", "options": ["George Orwell", "J.K. Rowling", "Ernest Hemingway", "Jane Austen"], "answer": "George Orwell"}
        ]
        self.current_index = 0

    def get_current_question(self):
        return self.questions[self.current_index]

    def next_question(self):
        self.current_index += 1
        return self.current_index < len(self.questions)
