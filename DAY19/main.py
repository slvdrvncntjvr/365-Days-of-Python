import curses
import random
from time import sleep

emotions = {
    "happiness": 50,
    "sadness": 50,
    "anger": 50,
    "calmness": 50
}

COLOR_MAP = {
    "happiness": curses.COLOR_YELLOW,
    "sadness": curses.COLOR_BLUE,
    "anger": curses.COLOR_RED,
    "calmness": curses.COLOR_GREEN
}

EVENT_IMPACT = {
    "positive": {"happiness": (10, 20), "calmness": (5, 15)},
    "negative": {"sadness": (10, 20), "anger": (5, 15)}
}

DECAY_RATE = 1
emotion_history = []

def adjust_emotions(emotion, value):
    emotions[emotion] = max(0, min(100, emotions[emotion] + value))

def decay_emotions():
    for emotion in emotions:
        emotions[emotion] = max(0, emotions[emotion] - DECAY_RATE)

def get_dominant_emotion():
    return max(emotions, key=emotions.get)

def emotion_feedback():
    dominant = get_dominant_emotion()
    feedback_map = {
        "happiness": "I'm feeling joyful! Life is bright right now.",
        "sadness": "I'm in a bit of a gloomy mood. Can we try something uplifting?",
        "anger": "I'm feeling fiery and frustrated. Let's cool down a bit.",
        "calmness": "I'm calm and serene. Everything is at peace."
    }
    return feedback_map[dominant]

def render_emotions(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "Human Emotion Simulator", curses.A_BOLD)
    stdscr.addstr(3, 2, "Current Emotions:")

    y = 5
    for emotion, value in emotions.items():
        stdscr.addstr(y, 2, f"{emotion.capitalize()}: ")
        bar_length = value // 2
        color_pair = list(COLOR_MAP.keys()).index(emotion) + 1
        stdscr.addstr(y, 15, "#" * bar_length, curses.color_pair(color_pair))
        y += 1

    stdscr.addstr(y + 1, 2, f"Dominant Emotion: {get_dominant_emotion().capitalize()}")
    stdscr.addstr(y + 3, 2, "Feedback:")
    stdscr.addstr(y + 4, 4, emotion_feedback())
    stdscr.addstr(y + 6, 2, "Type an event (positive/negative) or 'exit' to quit: ")
    stdscr.refresh()

def log_emotion_history():
    history_entry = f"H: {emotions['happiness']}, S: {emotions['sadness']}, A: {emotions['anger']}, C: {emotions['calmness']}"
    emotion_history.append(history_entry)

def display_emotion_history(stdscr):
    stdscr.addstr(10, 2, "Emotion History:")
    for idx, entry in enumerate(emotion_history[-5:], start=1):
        stdscr.addstr(10 + idx, 2, entry)
    stdscr.refresh()

def main(stdscr):
    curses.start_color()
    for idx, emotion in enumerate(COLOR_MAP.keys()):
        curses.init_pair(idx + 1, COLOR_MAP[emotion], curses.COLOR_BLACK)

    stdscr.nodelay(False)
    stdscr.keypad(True)
    curses.curs_set(1)

    while True:
        decay_emotions()
        render_emotions(stdscr)
        display_emotion_history(stdscr)
        
        event_type = stdscr.getstr().decode("utf-8").strip().lower()
        if event_type == "exit":
            break
        elif event_type in EVENT_IMPACT:
            for emotion, (low, high) in EVENT_IMPACT[event_type].items():
                impact = random.randint(low, high)
                adjust_emotions(emotion, impact if event_type == "positive" else -impact)
            log_emotion_history()
        else:
            stdscr.addstr(15, 2, "Invalid input! Type 'positive', 'negative', or 'exit'.")
            stdscr.refresh()
            sleep( 2)

if __name__ == "__main__":
    curses.wrapper(main)