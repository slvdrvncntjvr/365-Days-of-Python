import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageDraw, ImageFont

SAVE_DIR = "generated_art"
os.makedirs(SAVE_DIR, exist_ok=True)

class TextToArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Text-to-Art Generator")
        self.root.geometry("600x400")

        title = tk.Label(root, text="Text-to-Art Generator (somehow)", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        prompt_label = tk.Label(root, text="Enter a prompt to inspire your art: (keywords)", font=("Arial", 12))
        prompt_label.pack(pady=5)

        
        self.prompt_input = tk.Entry(root, font=("Arial", 12), width=40)
        self.prompt_input.pack(pady=5)

        generate_button = ttk.Button(root, text="Generate", command=self.generate_art)
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
        
        img_size = (500, 500)
        img = Image.new("RGB", img_size, "white")
        draw = ImageDraw.Draw(img)

        
        theme_map = {
            "sunset": {"colors": ["#FF4500", "#FF6347", "#FFD700"], "shapes": ["ellipse", "rectangle"]},
            "ocean": {"colors": ["#1E90FF", "#00CED1", "#4682B4"], "shapes": ["ellipse", "line"]},
            "forest": {"colors": ["#228B22", "#556B2F", "#8FBC8F"], "shapes": ["rectangle", "line"]},
            "love": {"colors": ["#FF69B4", "#FF1493", "#FFC0CB"], "shapes": ["ellipse", "rectangle"]},
            "galaxy": {"colors": ["#8A2BE2", "#4B0082", "#483D8B"], "shapes": ["ellipse", "line"]},
            "default": {"colors": ["#000000", "#808080", "#FFFFFF"], "shapes": ["ellipse", "rectangle", "line"]}
            }

        selected_theme = theme_map.get(
            next((key for key in theme_map if key in prompt.lower()), "default")
        )

        for _ in range(50):  
            shape_type = random.choice(selected_theme["shapes"])
            color = random.choice(selected_theme["colors"])

            x1, y1 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
            x2, y2 = random.randint(0, img_size[0]), random.randint(0, img_size[1])

            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            if shape_type == "ellipse":
                draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)
            elif shape_type == "rectangle":
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)
            elif shape_type == "line":
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))

        
        font = ImageFont.load_default()
        draw.text((10, img_size[1] - 20), prompt, fill="black", font=font)

        
        filename = f"{SAVE_DIR}/{prompt.replace(' ', '_')}_{random.randint(1000, 9999)}.png"
        img.save(filename)

        return filename


    def display_art(self, art_file):
        img = Image.open(art_file).resize((300, 300))
        self.tk_img = tk.PhotoImage(file=art_file) 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToArtApp(root)
    root.mainloop()
