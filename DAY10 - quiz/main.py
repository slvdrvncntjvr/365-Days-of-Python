from gui import QuizApp
from quiz import QuestionBank

if __name__ == "__main__":
    question_bank = QuestionBank()
    app = QuizApp(question_bank)
    app.run()
