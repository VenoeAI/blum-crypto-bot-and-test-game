import tkinter as tk
from tkinter import simpledialog, messagebox
import pyautogui
import threading
import time
from PIL import ImageGrab
import numpy as np

class ScreenRegionClickBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Region Click Bot")
        
        self.region = None
        self.rgba_value = None
        self.monitoring = False
        self.stop_event = threading.Event()

        self.info_label = tk.Label(root, text="Enter screen region (format: top,left,width,height):")
        self.info_label.pack(pady=5)

        self.region_entry = tk.Entry(root)
        self.region_entry.pack(pady=5)

        self.done_button = tk.Button(root, text="Done", command=self.validate_region)
        self.done_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring, state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.root.attributes('-topmost', True)

    def validate_region(self):
        region_input = self.region_entry.get()
        try:
            self.region = list(map(int, region_input.split(',')))
            if len(self.region) != 4:
                raise ValueError("Invalid number of arguments")
            if any(x < 0 for x in self.region[2:]):
                raise ValueError("Width and height must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return

        self.get_rgba_value()

    def get_rgba_value(self):
        rgba_string = simpledialog.askstring(
            "Input",
            "Enter RGBA value (format: R,G,B[,A]). Examples:\n"
            " - 255,0,0,255 for fully opaque red\n"
            " - 0,255,0 for fully opaque green (default alpha=255)"
        )
        if rgba_string is None:
            return
        values = list(map(int, rgba_string.split(',')))
        if len(values) == 3:
            values.append(255)  # Default alpha value
        self.rgba_value = tuple(values)
        self.start_button.config(state=tk.NORMAL)

    def start_monitoring(self):
        self.monitoring = True
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.info_label.config(text="Monitoring started.")

        self.monitor_thread = threading.Thread(target=self.monitor_region)
        self.monitor_thread.start()
        
        self.root.after(20000, self.auto_stop)

    def auto_stop(self):
        if self.monitoring:
            self.stop_monitoring()

    def stop_monitoring(self):
        self.monitoring = False
        self.stop_event.set()
        self.info_label.config(text="Monitoring stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.monitor_thread.join()

    def monitor_region(self):
        tolerance = 30  # Adjust this value as needed
        screen_region = (
            self.region[1], self.region[0], 
            self.region[1] + self.region[2], self.region[0] + self.region[3]
        )
        while self.monitoring and not self.stop_event.is_set():
            screenshot = ImageGrab.grab(bbox=screen_region)
            screenshot = np.array(screenshot)
            rgba_diff = np.abs(screenshot[..., :3] - np.array(self.rgba_value[:3]))  # Exclude alpha channel for comparison
            match_mask = np.all(rgba_diff <= tolerance, axis=-1)
            match_pixels = np.argwhere(match_mask)
            for x, y in match_pixels:
                pyautogui.click(self.region[1] + x, self.region[0] + y)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRegionClickBot(root)
    root.mainloop()
