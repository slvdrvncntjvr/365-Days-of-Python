import tkinter as tk
from tkinter import ttk
from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from collections import Counter
import sqlite3
import os

# Initialize database
DAY_FOLDER = "DAY25"
DB_FILE = os.path.join(DAY_FOLDER, "database.db")

def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS typing_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word1 TEXT NOT NULL,
            word2 TEXT NOT NULL,
            count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def save_bigrams_to_db(words):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for word1, word2 in bigrams(words):
        cursor.execute("""
            SELECT count FROM typing_data WHERE word1 = ? AND word2 = ?
        """, (word1, word2))
        row = cursor.fetchone()

        if row:
            cursor.execute("""
                UPDATE typing_data SET count = count + 1 WHERE word1 = ? AND word2 = ?
            """, (word1, word2))
        else:
            cursor.execute("""
                INSERT INTO typing_data (word1, word2) VALUES (?, ?)
            """, (word1, word2))
    conn.commit()
    conn.close()

def get_suggestions(last_word):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word2 FROM typing_data WHERE word1 = ? ORDER BY count DESC LIMIT 3
    """, (last_word,))
    suggestions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return suggestions

# GUI Application
class TypingAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Typing Assistant")
        self.root.geometry("800x400")

        self.history = []

        # Entry widget for typing
        self.text_input = tk.Entry(self.root, font=("Arial", 14))
        self.text_input.pack(pady=20, fill=tk.X, padx=10)
        self.text_input.bind("<KeyRelease>", self.on_key_release)

        # Suggestions label
        self.suggestions_label = tk.Label(self.root, text="Suggestions: ", font=("Arial", 12), anchor="w")
        self.suggestions_label.pack(fill=tk.X, padx=10)

        # Typed text display
        self.text_display = tk.Text(self.root, font=("Arial", 12), wrap=tk.WORD, state=tk.DISABLED, height=10)
        self.text_display.pack(pady=20, fill=tk.BOTH, padx=10, expand=True)

        # Save Button
        save_button = ttk.Button(self.root, text="Save Text", command=self.save_text)
        save_button.pack(pady=10)

    def on_key_release(self, event):
        typed_text = self.text_input.get().strip()
        if typed_text and event.keysym == "space":
            # Tokenize and process
            words = word_tokenize(typed_text)
            if len(words) > 1:
                save_bigrams_to_db(words[-2:])
            self.history.extend(words)

            # Clear the input
            self.update_display()
            self.text_input.delete(0, tk.END)

        elif typed_text:
            # Provide suggestions
            words = word_tokenize(typed_text)
            last_word = words[-1] if words else ""
            suggestions = get_suggestions(last_word)
            self.suggestions_label.config(text=f"Suggestions: {', '.join(suggestions)}")

    def update_display(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, " ".join(self.history))
        self.text_display.config(state=tk.DISABLED)

    def save_text(self):
        with open("typed_text.txt", "w", encoding="utf-8") as file:
            file.write(" ".join(self.history))
        tk.messagebox.showinfo("Saved", "Your text has been saved!")

# Initialize
if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        initialize_database()

    root = tk.Tk()
    app = TypingAssistantApp(root)
    root.mainloop()
