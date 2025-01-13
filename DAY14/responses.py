import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import os

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
                "Sorry, I don't know how to respond to that."]
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
    "favorite": "color"
}

def clean_and_tokenize(input_text):
    tokens = word_tokenize(input_text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def get_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return random.choice(["Hi there!", "Hello!", "Hey!"])
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "name" in user_input:
        return "I'm Chatpy, your friendly chatbot."
    elif "favorite color" in user_input:
        return "Colors are fascinating, but I think blue is calming!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm not sure I understand. Can you rephrase that?"
