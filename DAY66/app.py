import tkinter as tk
from PIL import Image, ImageTk
import math
import random

WIDTH, HEIGHT = 800, 600
MAX_ITER = 100
RE_START, RE_END = -2.0, 1.0
IM_START, IM_END = -1.0, 1.0

class MandelbrotExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mandelbrot Set Explorer")
        self.width = WIDTH
        self.height = HEIGHT
        self.max_iter = MAX_ITER
        self.re_start = RE_START
        self.re_end = RE_END
        self.im_start = IM_START
        self.im_end = IM_END
        self.zoom_factor = 0.5
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas_img = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.draw_mandelbrot()
        self.canvas.bind("<Button-1>", self.zoom_in)
        self.canvas.bind("<Button-3>", self.zoom_out)

    def draw_mandelbrot(self):
        for x in range(self.width):
            for y in range(self.height):
                c_re = self.re_start + (x / self.width) * (self.re_end - self.re_start)
                c_im = self.im_start + (y / self.height) * (self.im_end - self.im_start)
                c = complex(c_re, c_im)
                z = 0
                n = 0
                while abs(z) <= 2 and n < self.max_iter:
                    z = z * z + c
                    n += 1
                color = 255 - int(n * 255 / self.max_iter)
                self.image.putpixel((x, y), (color, color, color))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_img, image=self.photo)
        self.canvas.update()

    def zoom_in(self, event):
        click_x, click_y = event.x, event.y
        center_re = self.re_start + (click_x / self.width) * (self.re_end - self.re_start)
        center_im = self.im_start + (click_y / self.height) * (self.im_end - self.im_start)
        re_width = (self.re_end - self.re_start) * self.zoom_factor
        im_height = (self.im_end - self.im_start) * self.zoom_factor
        self.re_start = center_re - re_width / 2
        self.re_end = center_re + re_width / 2
        self.im_start = center_im - im_height / 2
        self.im_end = center_im + im_height / 2
        self.draw_mandelbrot()

    def zoom_out(self, event):
        click_x, click_y = event.x, event.y
        center_re = self.re_start + (click_x / self.width) * (self.re_end - self.re_start)
        center_im = self.im_start + (click_y / self.height) * (self.im_end - self.im_start)
        re_width = (self.re_end - self.re_start) / self.zoom_factor
        im_height = (self.im_end - self.im_start) / self.zoom_factor
        self.re_start = center_re - re_width / 2
        self.re_end = center_re + re_width / 2
        self.im_start = center_im - im_height / 2
        self.im_end = center_im + im_height / 2
        self.draw_mandelbrot()

if __name__ == "__main__":
    root = tk.Tk()
    app = MandelbrotExplorer(root)
    root.mainloop()
