import tkinter as tk
from PIL import ImageGrab

class PixelColorBot:
    def __init__(self, master):
        self.master = master
        self.master.title("Pixel Color Bot")
        self.master.attributes('-alpha', 0.5)  # Set transparency

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}+0+0")  # Set fullscreen

        self.canvas = tk.Canvas(master, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.get_pixel_color)

    def get_pixel_color(self, event):
        x, y = event.x, event.y
        screenshot = ImageGrab.grab()
        pixel_color = screenshot.getpixel((x, y))
        rgb_string = f"RGB: {pixel_color[0]}, {pixel_color[1]}, {pixel_color[2]}"

        self.canvas.create_text(x, y, text=rgb_string, fill='#000000', anchor=tk.SW)

def main():
    root = tk.Tk()
    app = PixelColorBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
