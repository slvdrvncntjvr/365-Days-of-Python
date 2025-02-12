from story_manager import load_story, get_story_segment
from nlp_processor import process_choice

def main():
    story = load_story('story.json')
    print(story["start"]["text"])

    while True:
        user_input = input("Your choice: ")
        choice = process_choice(user_input)

        if choice == "unknown":
            print("Sorry, I didn't understand that. Please choose 'left' or 'right'.")
            continue

        segment = get_story_segment(story, choice)
        print(segment)

        break

if __name__ == "__main__":
    main()