from responses import get_response

def main():
    print("Chatbot: Hi! I'm Chatpy, your friendly chatbot. Type 'bye' to end the chat.")
    
    while True:
        user_input = input("\nYou: ").strip().lower()
        
        if user_input == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        response = get_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
# to rework