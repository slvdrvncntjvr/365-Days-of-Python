import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageDraw

SAVE_DIR = "generated_art"
os.makedirs(SAVE_DIR, exist_ok=True)

class TextToArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Text-to-Art Generator")
        self.root.geometry("600x400")

        title = tk.Label(root, text="Text-to-Art Generator", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        prompt_label = tk.Label(root, text="Enter a prompt to inspire your art:", font=("Arial", 12))
        prompt_label.pack(pady=5)

        
        self.prompt_input = tk.Entry(root, font=("Arial", 12), width=40)
        self.prompt_input.pack(pady=5)

        generate_button = ttk.Button(root, text="Generate Art", command=self.generate_art)
        generate_button.pack(pady=20)

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(pady=10)

    def generate_art(self):
        prompt = self.prompt_input.get().strip()
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt!")
            return

        art_file = self.create_art(prompt)

        self.display_art(art_file)

        messagebox.showinfo("Success", f"Art generated and saved as {art_file}")

    def create_art(self, prompt):
        """Generates abstract art based on the inputt prompt."""
      
        img_size = (300, 300)
        img = Image.new("RGB", img_size, "white")
        draw = ImageDraw.Draw(img)

        #hashing
        random.seed(hash(prompt))

        for _ in range(50): 
            shape_type = random.choice(["ellipse", "rectangle", "line"])
            x1, y1 = random.randint(0, 300), random.randint(0, 300)
            x2, y2 = random.randint(0, 300), random.randint(0, 300)
            color = tuple(random.choices(range(256), k=3)) 

            

            if shape_type == "ellipse":
                draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)
            elif shape_type == "rectangle":
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)
            elif shape_type == "line":
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))

        filename = f"{SAVE_DIR}/{prompt.replace(' ', '_')}_{random.randint(1000, 9999)}.png"
        img.save(filename)

        return filename

    def display_art(self, art_file):
        """Displaying generated art in the canvas."""
        img = Image.open(art_file).resize((300, 300))
        self.tk_img = tk.PhotoImage(file=art_file) 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToArtApp(root)
    root.mainloop()
