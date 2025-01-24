import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
from tkinter.scrolledtext import ScrolledText

def load_markdown_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        html_content = markdown.markdown(markdown_content)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, html_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
app = tk.Tk()
app.title("Markdown Blog Viewer")
app.geometry("800x600")

menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open Markdown File", command=load_markdown_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

text_widget = ScrolledText(app, wrap=tk.WORD, font=("Arial", 12))
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

app.mainloop()
