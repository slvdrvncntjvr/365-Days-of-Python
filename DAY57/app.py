#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
import sys

QUESTIONS = [
    "What is your name?",
    "What is your favorite hobby?",
    "What is your dream career?",
    "Which city would you like to live in?",
    "What is your favorite food?"
]

EVENT_TEMPLATES = [
    "At the age of {age}, {name} discovered a passion for {hobby}.",
    "After years of dedication, {name} became a renowned {career}.",
    "Living in {city}, {name} experienced countless adventures and made lifelong memories.",
    "One unforgettable day, while enjoying {food}, {name} realized that life's true joy lies in the simple moments.",
    "{name}'s journey took an unexpected turn when they combined their love for {hobby} with their career as a {career} in {city}.",
    "Over time, {name} learned that sharing {food} with loved ones was the secret to lasting happiness."
]

def generate_life_story(answers):
    name, hobby, career, city, food = answers
    story = []
    current_age = 18
    for template in EVENT_TEMPLATES:
        age_increment = random.randint(5, 10)
        current_age += age_increment
        story.append(template.format(age=current_age, name=name, hobby=hobby, career=career, city=city, food=food))
    return "\n\n".join(story)

class LifePathSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Path Simulator")
        self.root.geometry("600x600")
        self.answers = []
        self.current_question = 0
        self.create_widgets()

    def create_widgets(self):
        self.question_label = ttk.Label(self.root, text=QUESTIONS[self.current_question], font=("Arial", 14))
        self.question_label.pack(pady=20)
        self.answer_entry = ttk.Entry(self.root, width=50, font=("Arial", 12))
        self.answer_entry.pack(pady=10)
        self.next_button = ttk.Button(self.root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)
        self.story_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.story_text.pack(pady=20, fill="both", expand=True)
        self.story_text.config(state=tk.DISABLED)

    def next_question(self):
        answer = self.answer_entry.get().strip()
        if not answer:
            messagebox.showwarning("Input Error", "Please provide an answer!")
            return
        self.answers.append(answer)
        self.answer_entry.delete(0, tk.END)
        self.current_question += 1
        if self.current_question < len(QUESTIONS):
            self.question_label.config(text=QUESTIONS[self.current_question])
        else:
            self.generate_story()

    def generate_story(self):
        story = generate_life_story(self.answers)
        self.question_label.config(text="Your Life Path Story:")
        self.answer_entry.destroy()
        self.next_button.destroy()
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, story)
        self.story_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = LifePathSimulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
