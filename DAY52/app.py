import re
import sys
import random
from collections import Counter, defaultdict
import json
import os

try:
    import nltk
    from nltk import word_tokenize, sent_tokenize
except ImportError:
    print("NLTK not installed. Installing now...")
    os.system("pip install nltk")
    import nltk
    from nltk import word_tokenize, sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    frequency = Counter(words)
    avg_length = sum(len(word) for word in words) / len(words) if words else 0
    longest = max(words, key=len) if words else ""
    palindromes = sorted([word for word in set(words) if len(word) > 1 and word == word[::-1]])
    return frequency, avg_length, longest, palindromes

def display_frequency(freq, top=10):
    common = freq.most_common(top)
    print("\nTop {} most common words:".format(top))
    for word, count in common:
        print(f"{word}: {count}")

def generate_markov(text, n=2, length=100):
    words = word_tokenize(text.lower())
    if len(words) < n:
        return text
    model = defaultdict(list)
    for i in range(len(words) - n):
        key = tuple(words[i:i+n])
        model[key].append(words[i+n])
    current = random.choice(list(model.keys()))
    output = list(current)
    for i in range(length - n):
        next_words = model.get(current)
        if not next_words:
            current = random.choice(list(model.keys()))
            output.extend(current)
        else:
            next_word = random.choice(next_words)
            output.append(next_word)
            current = tuple(output[-n:])
    return " ".join(output)

def load_dictionary():
    return [
        "listen", "silent", "enlist", "inlets", "google", "gogole",
        "evil", "vile", "veil", "live", "dare", "read", "dear", "adore", "radio",
        "brag", "grab", "dusty", "study", "night", "thing"
    ]

def find_anagrams(word, dictionary):
    word = word.lower()
    sorted_word = ''.join(sorted(word))
    anagrams = [w for w in dictionary if w != word and ''.join(sorted(w)) == sorted_word]
    return anagrams

def main_menu():
    print("\n=== Lexical Alchemist – The Word Wizard ===")
    print("1. Load text from file")
    print("2. Analyze loaded text")
    print("3. Generate text using Markov chain")
    print("4. Find anagrams for a word")
    print("5. Exit")

def main():
    text = ""
    dictionary = load_dictionary()
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            file_path = input("Enter the file path: ").strip()
            try:
                text = load_text(file_path)
                print("Text loaded successfully!")
            except Exception as e:
                print(f"Error loading file: {e}")
        elif choice == "2":
            if not text:
                print("No text loaded. Please load text first.")
                continue
            freq, avg_len, longest, palindromes = analyze_text(text)
            print(f"\nAverage word length: {avg_len:.2f}")
            print(f"Longest word: {longest}")
            print(f"Palindromes: {', '.join(palindromes) if palindromes else 'None'}")
            display_frequency(freq, top=10)
        elif choice == "3":
            if not text:
                print("No text loaded. Please load text first.")
                continue
            generated = generate_markov(text, n=2, length=100)
            print("\nGenerated Text:\n")
            print(generated)
        elif choice == "4":
            word = input("Enter a word to find anagrams: ").strip()
            anagrams = find_anagrams(word, dictionary)
            print(f"Anagrams for '{word}': {', '.join(anagrams) if anagrams else 'None found'}")
        elif choice == "5":
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
