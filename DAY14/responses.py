import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

RESPONSES = {
    "greeting": ["Hello!", "Hi there!", "Hey!", "Hi! How can I help you?"],
    "name": ["I'm Chatpy, your friendly chatbot.", "They call me Chatpy. What's yours?"],
    "mood": ["I'm just a bunch of code, but I'm always happy to chat with you!", 
             "I don't have feelings, but I hope you're having a great day!"],
    "color": ["I like all colors, but I think blue is calming.", 
              "Colors are fascinating, aren't they?"],
    "unknown": ["I'm not sure I understand. Can you rephrase that?", 
                "Sorry, I don't know how to respond to that."],
    "yue": ["Are you talking about the love of your life? How is she?", 
              "I hope Yue is doing well. She sounds like a great person!"]
}

KEYWORDS = {
    "hello": "greeting",
    "hi": "greeting",
    "name": "name",
    "who": "name",
    "how": "mood",
    "feeling": "mood",
    "color": "color",
    "favourite": "color",
    "favorite": "color",
    "yue": "yue",
    "Yue": "yue"
}

# hindi ko na import punkt 
# remind self to import punkt
def clean_and_tokenize(input_text):
    tokens = word_tokenize(input_text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def get_response(user_input):
    tokens = clean_and_tokenize(user_input)
    
    for token in tokens:
        if token in KEYWORDS:
            category = KEYWORDS[token]
            return random.choice(RESPONSES[category])
    
    return random.choice(RESPONSES["unknown"])

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