import tkinter as tk

class ScreenRegionSelector(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Screen Region Selector")
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)  # Make the window semi-transparent
        self.config(cursor="cross")

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.winfo_pointerx() - self.winfo_rootx()
        self.start_y = self.winfo_pointery() - self.winfo_rooty()
        
        if self.rect:
            self.canvas.delete(self.rect)

        self.canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        current_x = self.winfo_pointerx() - self.winfo_rootx()
        current_y = self.winfo_pointery() - self.winfo_rooty()
        self.canvas.coords(self.rect, self.start_x, self.start_y, current_x, current_y)

    def on_button_release(self, event):
        end_x = self.winfo_pointerx() - self.winfo_rootx()
        end_y = self.winfo_pointery() - self.winfo_rooty()

        top = min(self.start_y, end_y)
        left = min(self.start_x, end_x)
        width = abs(self.start_x - end_x)
        height = abs(self.start_y - end_y)

        screen_region = {"top": top, "left": left, "width": width, "height": height}
        print(screen_region)

        self.quit()

if __name__ == "__main__":
    app = ScreenRegionSelector()
    app.mainloop()
