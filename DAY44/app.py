import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

SAVE_DIR = "generated_qrcodes"
os.makedirs(SAVE_DIR, exist_ok=True)

SECRET_KEY = b'JrU0wJc_eJhD_R0I9p_JD_6z7rbdh6aD6Xghz23dFo4='
cipher = Fernet(SECRET_KEY)

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure QR Code Generator")
        self.root.geometry("500x600")
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Enter text to encrypt and generate QR code", font=("Arial", 14))
        self.label.pack(pady=10)
        self.entry = ttk.Entry(self.root, width=50, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.generate_button = ttk.Button(self.root, text="Generate QR Code", command=self.generate_qr)
        self.generate_button.pack(pady=10)
        self.image_label = ttk.Label(self.root)
        self.image_label.pack(pady=10)

    def generate_qr(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text")
            return
        encrypted_text = cipher.encrypt(text.encode()).decode()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(encrypted_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = os.path.join(SAVE_DIR, f"qr_{len(text)}_{os.getpid()}.png")
        img.save(filename)
        img = img.resize((300, 300))
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)
        messagebox.showinfo("Success", f"QR code generated and saved as {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
