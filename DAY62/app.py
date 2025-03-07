import random
import time
import os

class PythonJourney:
    def __init__(self):
        self.day = 61
        self.learning_milestones = [
            "Basics of Python - Variables, Types, and Operators",
            "Control Structures - If-Else, Loops, and List Comprehensions",
            "Functions, Arguments, and Return Values",
            "File I/O Operations and Handling",
            "Working with Libraries (random, datetime, os)",
            "Object-Oriented Programming (Classes, Objects, Inheritance)",
            "Regular Expressions and Patterns",
            "Data Structures (Lists, Tuples, Sets, Dictionaries)",
            "Error Handling and Exceptions",
            "Building Small Projects"
        ]
        self.learning_progress = 0.7  
        self.messages = [
            "Every error is a learning opportunity.",
            "One line of code today could spark a thousand possibilities tomorrow.",
            "Remember: Python doesn't make mistakes, you do. But you're getting better at it!",
            "Your progress is reflected in the way you think about code.",
            "Day 61 is just another step in mastering Python. Keep going!"
        ]
    
    def show_welcome(self):
        """Display a welcome message, including the day and progress."""
        print("\nWelcome to Day", self.day, "of your Python learning journey!")
        print("You've made amazing progress so far. Keep going!")
        self.display_milestones()
    
    def display_milestones(self):
        """Show milestones based on progress."""
        print("\nKey Milestones Achieved So Far:")
        for idx, milestone in enumerate(self.learning_milestones):
            print(f"{idx + 1}. {milestone}")
        
        print(f"\nCurrent progress: {self.learning_progress * 100}%")
        print(f"Keep pushing forward! Let's see what comes next.")
    
    def random_quote(self):
        """Get a random inspirational quote about learning and programming."""
        return random.choice(self.messages)
    
    def journey_summary(self):
        """Print a summary of the learning journey."""
        summary = f"\nOn Day {self.day}, you are improving rapidly in Python.\n"
        summary += f"You've explored various topics, from basic syntax to complex algorithms.\n"
        summary += "Let’s visualize your journey so far with a progress bar."
        return summary
    
    def display_progress_bar(self):
        """Create a visual progress bar to show how far you've come."""
        total = 50 
        filled = int(self.learning_progress * total)
        bar = '█' * filled + '-' * (total - filled)
        print(f"\nProgress: [{bar}] {self.learning_progress * 100:.1f}%")
    
    def explore_new_topics(self):
        """Encourage learning new topics to challenge yourself."""
        topics = [
            "Machine Learning and Data Science",
            "Web Development with Flask or Django",
            "API Development and Integration",
            "Database Connectivity with SQL and Python",
            "GUI Development with Tkinter or PyQt"
        ]
        print("\nIt's time to start diving into these new topics to continue your learning!")
        print("Here are some suggestions to push the envelope on your journey:")
        for idx, topic in enumerate(topics, 1):
            print(f"{idx}. {topic}")
    
    def python_art(self):
        """Generate a cool Python-based ASCII art representation."""
        python_art = """
          _____     _           _    _         
         |  __ \   (_)         | |  (_)        
         | |__) |__ _ _ __ ___ | |__ _ _ __ ___ 
         |  ___/ _` | '_ ` _ \| '_ \ | '__/ _ \\
         | |  | (_| | | | | | | |_) | | | |  __/
         |_|   \__,_|_| |_| |_|_.__/|_|_|  \___|
        """
        print("\nHere's a fun Python ASCII art to motivate you further:")
        print(python_art)
    
    def interactive_quiz(self):
        """A little interactive quiz to test what you've learned so far."""
        print("\nLet’s see how well you've learned Python so far!")
        questions = {
            "What is the method to add an item to a list in Python?": ["append", "insert", "add"],
            "Which keyword is used to handle exceptions in Python?": ["try", "catch", "except"],
            "How do you define a class in Python?": ["class MyClass:", "def MyClass():", "function MyClass():"],
            "Which function is used to generate random numbers in Python?": ["random.random()", "rand()", "randomize()"]
        }
        
        score = 0
        for question, options in questions.items():
            print(f"\n{question}")
            print("Options:", ", ".join(options))
            answer = input("Your answer: ").strip().lower()
            if answer == options[0]:
                print("Correct!")
                score += 1
            else:
                print("Oops! That's not correct.")
        
        print(f"\nYour quiz score: {score}/{len(questions)}")
        print("Time to review and keep growing!")
    
    def future_expectations(self):
        """Create a short-term projection on the Python journey."""
        print("\nLooking Ahead: What's next?")
        print("In the next 60 days, you could be working with frameworks, contributing to open-source, or building your own startup.")
        print("Stay tuned for a lifetime of opportunities!")
    
    def end_journey_message(self):
        """A message to signify that this is just one milestone."""
        print("\nRemember, this journey never ends. Keep coding, keep learning, and the world will open up to you.")
        print("Day 61 is done. What's next? Let’s go to Day 62!")

def clear_screen():
    """Clear the screen after each stage for a neat presentation."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function to start the Python journey experience."""
    journey = PythonJourney()
    clear_screen()
    journey.show_welcome()
    
    time.sleep(2)
    print(journey.journey_summary())
    time.sleep(2)
    journey.display_progress_bar()
    
    
    time.sleep(2)
    print("\nMotivational Message:", journey.random_quote())
    

    time.sleep(2)
    journey.explore_new_topics()
    
    # 
    time.sleep(2)
    journey.python_art()

    time.sleep(2)
    journey.interactive_quiz()
    
    
    time.sleep(2)
    journey.future_expectations()
    
    time.sleep(2)
    journey.end_journey_message()

if __name__ == "__main__":
    main()
