import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from storage import load_data, save_data

POMODORO_DURATION = 25 * 60  

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Task Manager")
        self.data = load_data()
        self.current_task = None
        self.timer_running = False
        self.remaining_time = 0
        self.create_widgets()
        self.update_task_list()
        self.update_stats()

    def create_widgets(self):
        task_frame = ttk.Frame(self.root)
        task_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(task_frame, text="New Task:").pack(side="left")
        self.task_entry = ttk.Entry(task_frame)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(task_frame, text="Add Task", command=self.add_task).pack(side="left", padx=5)

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.task_listbox = tk.Listbox(list_frame, height=10)
        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        self.timer_label = ttk.Label(self.root, text="Timer: 00:00", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill="x")
        ttk.Button(control_frame, text="Start Pomodoro", command=self.start_pomodoro).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Stop Timer", command=self.stop_timer).pack(side="left", padx=5)

        self.stats_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.stats_label.pack(pady=10)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.data["tasks"].append(task_text)
            save_data(self.data)
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.data["tasks"]:
            self.task_listbox.insert(tk.END, task)

    def update_stats(self):
        sessions = self.data.get("sessions", {})
        total_sessions = sum(sessions.values()) if sessions else 0
        self.stats_label.config(text=f"Total Pomodoro Sessions Completed: {total_sessions}")

    def start_pomodoro(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task.")
            return
        self.current_task = self.task_listbox.get(selection[0])
        self.remaining_time = POMODORO_DURATION
        if not self.timer_running:
            self.timer_running = True
            threading.Thread(target=self.run_timer, daemon=True).start()

    def stop_timer(self):
        self.timer_running = False

    def run_timer(self):
        while self.timer_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_label.config(text=f"Timer: {time_format}")
            time.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time == 0:
            self.timer_label.config(text="Time's up!")
            self.complete_session()

    def complete_session(self):
        self.timer_running = False
        sessions = self.data.get("sessions", {})
        sessions[self.current_task] = sessions.get(self.current_task, 0) + 1
        self.data["sessions"] = sessions
        save_data(self.data)
        self.update_stats()
        messagebox.showinfo("Session Complete", f"Pomodoro session for '{self.current_task}' completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
