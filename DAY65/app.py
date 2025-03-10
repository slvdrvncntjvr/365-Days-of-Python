import tkinter as tk
import time
import pytz
from datetime import datetime
from math import pi, cos, sin

# Define cities and their time zones
CITIES = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Dubai": "Asia/Dubai",
}

# Function to get current time for a city
def get_time(city):
    tz = pytz.timezone(CITIES[city])
    return datetime.now(tz)

# Function to draw a clock
def draw_clock(canvas, x, y, city):
    canvas.create_oval(x-50, y-50, x+50, y+50, fill="white", outline="black", width=2)
    canvas.create_text(x, y+65, text=city, font=("Arial", 10, "bold"))

# Function to update clock hands
def update_clocks():
    canvas.delete("hands")
    for i, city in enumerate(CITIES):
        x, y = 150 + (i % 3) * 120, 100 + (i // 3) * 150
        time_now = get_time(city)
        draw_hands(canvas, x, y, time_now)
    root.after(1000, update_clocks)

# Function to draw clock hands
def draw_hands(canvas, x, y, time_now):
    hour, minute, second = time_now.hour % 12, time_now.minute, time_now.second
    second_angle = pi/2 - (second * 6) * pi/180
    minute_angle = pi/2 - (minute * 6) * pi/180
    hour_angle = pi/2 - ((hour * 30) + (minute * 0.5)) * pi/180
    
    canvas.create_line(x, y, x + 40 * cos(hour_angle), y - 40 * sin(hour_angle), width=4, tags="hands", fill="black")
    canvas.create_line(x, y, x + 45 * cos(minute_angle), y - 45 * sin(minute_angle), width=3, tags="hands", fill="blue")
    canvas.create_line(x, y, x + 50 * cos(second_angle), y - 50 * sin(second_angle), width=2, tags="hands", fill="red")

# Initialize Tkinter window
root = tk.Tk()
root.title("World Clock Visualizer")
canvas = tk.Canvas(root, width=400, height=300, bg="lightgray")
canvas.pack()

# Draw static clocks
for i, city in enumerate(CITIES):
    x, y = 150 + (i % 3) * 120, 100 + (i // 3) * 150
    draw_clock(canvas, x, y, city)

update_clocks()
root.mainloop()
