import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from color_extractor import extract_colors, get_palette_image, rgb_to_hex

SAVE_DIR = "generated_qrcodes"
os.makedirs(SAVE_DIR, exist_ok=True)

class ColorPaletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Color Palette Generator")
        self.root.geometry("600x650")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter image to generate its color palette", font=("Arial", 14))
        self.label.pack(pady=10)
        self.select_button = tk.Button(self.root, text="Select Image", command=self.load_image)
        self.select_button.pack(pady=10)
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        self.palette_label = tk.Label(self.root)
        self.palette_label.pack(pady=10)
        self.hex_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.hex_label.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file_path:
            return
        try:
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
            colors = extract_colors(file_path, num_colors=5)
            palette = get_palette_image(colors, swatch_size=50)
            self.tk_palette = ImageTk.PhotoImage(palette)
            self.palette_label.config(image=self.tk_palette)
            hex_codes = [rgb_to_hex(color) for color in colors]
            hex_text = "Hex Codes: " + ", ".join(hex_codes)
            self.hex_label.config(text=hex_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPaletteApp(root)
    root.mainloop()
