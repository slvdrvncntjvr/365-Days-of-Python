import tkinter as tk
from mood_data import moods
from spotify_helper import get_recommendations

def on_mood_select(mood):
    recommendations = get_recommendations(mood)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Recommended songs for {mood} mood:\n\n")
    for song, artist in recommendations:
        result_text.insert(tk.END, f"{song} by {artist}\n")

root = tk.Tk()
root.title("Mood-Based Music Recommender")
root.geometry("500x600")

title_label = tk.Label(root, text="Select Your Mood", font=("Arial", 18))
title_label.pack(pady=10)

for mood in moods.keys():
    button = tk.Button(root, text=mood.title(), command=lambda m=mood: on_mood_select(m))
    button.pack(pady=5)

result_text = tk.Text(root, wrap=tk.WORD, height=25, width=50)
result_text.pack(pady=10)

root.mainloop()
