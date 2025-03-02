import random
import re
import sys
from collections import defaultdict, Counter

CORPUS = """
Alice: Hi, how are you doing today?
Bob: I'm doing well, thank you! And how about you?
Alice: I'm feeling curious about what the future holds.
Bob: The future is full of endless possibilities.
Alice: Sometimes I wonder if we can predict what happens next.
Bob: Predictions are tricky, but our actions shape the future.
Alice: I think conversation is a window into the soul.
Bob: Indeed, every word reveals a part of who we are.
Alice: Do you believe that language can change lives?
Bob: Absolutely! Words have the power to inspire, heal, and transform.
Alice: That's truly fascinating.
Bob: Yes, conversations like these make every day extraordinary.
Alice: I wish more people could appreciate the beauty of words.
Bob: Words are the building blocks of our reality.
Alice: Thank you for sharing your thoughts.
Bob: My pleasure, it's always enlightening to talk.
"""

def tokenize_corpus(corpus):
    lines = corpus.strip().split("\n")
    dialogues = []
    for line in lines:
        if ":" in line:
            speaker, dialogue = line.split(":", 1)
            dialogue = dialogue.strip()
            if dialogue:
                dialogues.append(dialogue)
    tokens = []
    for dialogue in dialogues:
        tokens.extend(re.findall(r'\w+', dialogue.lower()))
    return tokens

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.model = defaultdict(list)
        self.start_sequences = []

    def train(self, tokens):
        if len(tokens) < self.order:
            return
        for i in range(len(tokens) - self.order):
            key = tuple(tokens[i:i+self.order])
            self.model[key].append(tokens[i+self.order])
            if i == 0 or tokens[i-1][-1] in ".!?":
                self.start_sequences.append(key)
        if not self.start_sequences:
            self.start_sequences = list(self.model.keys())

    def generate(self, length=20):
        if not self.model:
            return ""
        current = random.choice(self.start_sequences)
        output = list(current)
        for _ in range(length - self.order):
            key = tuple(output[-self.order:])
            next_words = self.model.get(key)
            if not next_words:
                break
            next_word = random.choice(next_words)
            output.append(next_word)
        sentence = " ".join(output)
        sentence = sentence.capitalize() + "."
        return sentence

def main():
    print("Welcome to Dialogue Alchemist – The Conversational Word Wizard!")
    print("This program simulates an interactive dialogue with a fictional character.")
    print("Type 'exit' to quit.\n")

    tokens = tokenize_corpus(CORPUS)
    markov = MarkovChain(order=2)
    markov.train(tokens)

    print("Let's start the conversation!\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        response = markov.generate(length=random.randint(10, 25))
        print("Alchemist:", response)

if __name__ == "__main__":
    main()
