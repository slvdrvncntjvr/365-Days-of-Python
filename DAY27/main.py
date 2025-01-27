import tkinter as tk
from tkinter import ttk
from random import randint
from threading import Thread
from time import sleep
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SocialMediaDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Engagement Dashboard")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    
        header = tk.Label(
            root, text="Social Media Engagement Dashboard", font=("Arial", 20, "bold")
        )
        header.pack(pady=10)


        self.metrics_frame = tk.Frame(root)
        self.metrics_frame.pack(pady=20)

        self.followers = tk.IntVar(value=randint(1000, 5000))
        self.likes = tk.IntVar(value=randint(500, 2000))
        self.comments = tk.IntVar(value=randint(100, 500))
        self.shares = tk.IntVar(value=randint(50, 200))

        self.create_metric("Followers", self.followers, 0)
        self.create_metric("Likes", self.likes, 1)
        self.create_metric("Comments", self.comments, 2)
        self.create_metric("Shares", self.shares, 3)

        booster_button = ttk.Button(
            root, text="Boost Engagement 🚀", command=self.boost_engagement
        )
        booster_button.pack(pady=10)

    
        trends_label = tk.Label(root, text="Engagement Trends", font=("Arial", 16, "bold"))
        trends_label.pack(pady=10)

        self.trends_frame = tk.Frame(root)
        self.trends_frame.pack()

        self.trends_chart = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.trends_chart.add_subplot(111)
        self.ax.bar(["Followers", "Likes", "Comments", "Shares"], 
                    [self.followers.get(), self.likes.get(), self.comments.get(), self.shares.get()], 
                    color=["blue", "green", "orange", "purple"])

        self.chart_canvas = FigureCanvasTkAgg(self.trends_chart, master=self.trends_frame)
        self.chart_canvas.get_tk_widget().pack()


        self.running = True
        self.start_live_updates()

    def create_metric(self, name, var, col):
        metric_frame = tk.Frame(self.metrics_frame)
        metric_frame.grid(row=0, column=col, padx=20)

        tk.Label(metric_frame, text=name, font=("Arial", 14, "bold")).pack()
        tk.Label(metric_frame, textvariable=var, font=("Arial", 18), fg="blue").pack()

    def boost_engagement(self):
        self.followers.set(self.followers.get() + randint(50, 200))
        self.likes.set(self.likes.get() + randint(20, 100))
        self.comments.set(self.comments.get() + randint(10, 50))
        self.shares.set(self.shares.get() + randint(5, 30))
        self.update_trends_chart()

    def update_trends_chart(self):
        self.ax.clear()
        self.ax.bar(["Followers", "Likes", "Comments", "Shares"], 
                    [self.followers.get(), self.likes.get(), self.comments.get(), self.shares.get()], 
                    color=["blue", "green", "orange", "purple"])
        self.chart_canvas.draw()

    def live_updates(self):
        while self.running:
            sleep(1)
            self.followers.set(self.followers.get() + randint(-5, 10))
            self.likes.set(self.likes.get() + randint(-2, 5))
            self.comments.set(self.comments.get() + randint(-1, 3))
            self.shares.set(self.shares.get() + randint(-1, 2))
            self.update_trends_chart()

    def start_live_updates(self):
        Thread(target=self.live_updates, daemon=True).start()

    def stop_live_updates(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaDashboard(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_live_updates)
    root.mainloop()
