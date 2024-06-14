import cv2
import numpy as np
from ultralytics import YOLO
import mss
import pyautogui
import random
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# Load YOLOv8 model
model = YOLO('best.pt')

# Global variables
screen_region = {'top': 100, 'left': 100, 'width': 800, 'height': 600}
detection_active = False
clicking_active = False
feedback_text = None

# Padding around detected objects to avoid accidental clicking
padding = 40

class ScreenRegionSelector(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
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
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)

        self.canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        current_x = event.x
        current_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, current_x, current_y)

    def on_button_release(self, event):
        end_x = event.x
        end_y = event.y

        top = min(self.start_y, end_y)
        left = min(self.start_x, end_x)
        width = abs(self.start_x - end_x)
        height = abs(self.start_y - end_y)

        screen_region = {"top": top, "left": left, "width": width, "height": height}
        self.callback(screen_region)
        self.destroy()

# Tkinter GUI
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Object Detection with YOLOv8")
        self.geometry("400x400")

        self.region_btn = tk.Button(self, text="Get Screen Region", command=self.open_screen_region_selector)
        self.region_btn.pack(pady=10)

        self.clicking_var = tk.BooleanVar()
        self.clicking_check = tk.Checkbutton(self, text="Enable Clicking", variable=self.clicking_var)
        self.clicking_check.pack(pady=5)

        self.start_btn = tk.Button(self, text="Start", command=self.start_detection)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_detection)
        self.stop_btn.pack(pady=10)

        self.feedback_label = tk.Label(self, text="Screen Region: None")
        self.feedback_label.pack(pady=5)

        self.feedback_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.feedback_text.pack(pady=10)
        self.feedback_text.config(state=tk.DISABLED)

    def open_screen_region_selector(self):
        self.withdraw()
        self.region_selector = ScreenRegionSelector(self, self.set_screen_region)
        self.region_selector.mainloop()
        self.deiconify()

    def set_screen_region(self, region):
        global screen_region
        screen_region = region
        self.feedback_label.config(text=f"Screen Region: {screen_region}")

    def start_detection(self):
        global detection_active, clicking_active
        detection_active = True
        clicking_active = self.clicking_var.get()
        self.run_detection()

    def stop_detection(self):
        global detection_active
        detection_active = False

    def run_detection(self):
        if not detection_active:
            return
        threading.Thread(target=self.detect_objects_loop).start()

    def detect_objects_loop(self):
        global detection_active
        with mss.mss() as sct:
            start_time = time.time()
            max_duration = 1 * 60  # 1 minute in seconds
            while detection_active:
                loop_start_time = time.time()
                detection_screenshot = sct.grab(screen_region)
                detection_image = np.array(detection_screenshot)
                detection_image = cv2.cvtColor(detection_image, cv2.COLOR_BGRA2BGR)

                results = model(detection_image)
                safe_areas = []
                for result in results:
                    boxes = result.boxes.xyxy.numpy()
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box)
                        safe_areas.append((x1 - padding, y1 - padding, x2 + padding, y2 + padding))
                        self.update_feedback(f"Detected object at: ({x1}, {y1}), ({x2}, {y2}) with confidence {result.boxes.conf.numpy()[0]:.2f}")

                if clicking_active:
                    self.generate_random_clicks(screen_region, safe_areas, num_clicks=10)

                loop_end_time = time.time()
                elapsed_time = loop_end_time - loop_start_time
                if elapsed_time < 1 / 60:
                    time.sleep(1 / 60 - elapsed_time)

                total_elapsed_time = time.time() - start_time
                if total_elapsed_time > max_duration:
                    detection_active = False

    def update_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        lines = self.feedback_text.get("1.0", tk.END).splitlines()
        if len(lines) >= 4:
            self.feedback_text.delete("1.0", "2.0")
        self.feedback_text.insert(tk.END, message + "\n")
        self.feedback_text.see(tk.END)
        self.feedback_text.config(state=tk.DISABLED)

    def generate_random_clicks(self, region, safe_areas, num_clicks):
        clicked_points = set()
        click_threads = []
        
        while len(click_threads) < num_clicks:
            x = random.randint(region['left'], region['left'] + region['width'] - 1)
            y = random.randint(region['top'], region['top'] + region['height'] - 1)
            
            safe = True
            for (x1, y1, x2, y2) in safe_areas:
                if x1 - padding <= x <= x2 + padding and y1 - padding <= y <= y2 + padding:
                    safe = False
                    break
            
            if safe and (x, y) not in clicked_points:
                clicked_points.add((x, y))
                thread = threading.Thread(target=click, args=(x, y))
                click_threads.append(thread)
        
        for thread in click_threads:
            thread.start()
        
        for thread in click_threads:
            thread.join()

def click(x, y):
    pyautogui.click(x, y)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
