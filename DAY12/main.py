import re
import math

def get_password_entropy(password):
    character_pool = 0
    
    if any(char.islower() for char in password):
        character_pool += 26
    if any(char.isupper() for char in password):
        character_pool += 26
    if any(char.isdigit() for char in password):
        character_pool += 10
    if any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        character_pool += 32
    if any(char.isspace() for char in password):
        character_pool += 1

    if character_pool == 0:  # Avoid division by zero
        return 0

    entropy = len(password) * math.log2(character_pool)
    return round(entropy, 2)

def check_password_strength(password):
    entropy_score = get_password_entropy(password)
    password_length = len(password)

    if password_length < 8:
        return "Weak: Password is too short. Use at least 8 characters."
    elif entropy_score < 40:
        return "Weak: Try mixing in uppercase, symbols, or numbers."
    elif entropy_score < 60:
        return "Moderate: Decent, but consider adding more complexity."
    elif entropy_score < 80:
        return "Strong: Great password! It’s secure."
    else:
        return "Wow, what a strong password! You're a security pro haha"

def main():
    print("=== Password Strength Checker ===")
    print("Entropy Threshold: \nOnline attacks: Require ~40 bits minimum. Offline attacks: Require ~80 bits or more.")
    password_input = input("Enter a password to check: ").strip()
    
    if not password_input:
        print("Error: Password cannot be blank!")
        return
    
    password_strength = check_password_strength(password_input)
    entropy_score = get_password_entropy(password_input)

    print(f"\nPassword Entropy: {entropy_score} bits")
    print(f"Strength Assessment: {password_strength}")

if __name__ == "__main__":
    main()
