import tkinter as tk
from tkinter import messagebox
from score_manager import ScoreManager

class QuizApp:
    def __init__(self, question_bank):
        self.question_bank = question_bank
        self.score_manager = ScoreManager()
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Quiz Game")

        # UI Elements
        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack()

        self.options_buttons = []
        for i in range(4):
            button = tk.Button(self.options_frame, text="", width=20, font=("Arial", 12), command=lambda idx=i: self.check_answer(idx))
            button.grid(row=i, column=0, pady=5)
            self.options_buttons.append(button)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.load_question()

    def load_question(self):
        question_data = self.question_bank.get_current_question()
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.options_buttons[i].config(text=option)

    def check_answer(self, idx):
        question_data = self.question_bank.get_current_question()
        selected_option = question_data["options"][idx]
        if selected_option == question_data["answer"]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror("Wrong!", "That's incorrect.")

        if not self.question_bank.next_question():
            self.end_quiz()
        else:
            self.load_question()

    def end_quiz(self):
        messagebox.showinfo("Quiz Finished!", f"Your final score is: {self.score}")
        self.score_manager.save_score(self.score)
        self.root.quit()

    def run(self):
        self.root.mainloop()
