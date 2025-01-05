import random

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def get_user_choice():
    while True:
        user_input = input("Enter your choice (rock, paper, scissors): ").lower()
        if user_input in ["rock", "paper", "scissors"]:
            return user_input
        print("Invalid input. Please choose rock, paper, or scissors.")

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "You win!"
    else:
        return "You lose!"

def main():
    print("Welcome to Rock, Paper, Scissors!")
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()

    print(f"\nYou chose: {user_choice}")
    print(f"The computer chose: {computer_choice}")

    result = determine_winner(user_choice, computer_choice)
    print(f"\n{result}")

if __name__ == "__main__":
    main()
