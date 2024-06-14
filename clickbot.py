import tkinter as tk
import pyautogui
import threading
import time

class RapidClickBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Rapid Click Bot")

        self.clicking = False
        self.stop_event = threading.Event()

        self.info_label = tk.Label(root, text="Press 'Start' to begin clicking.")
        self.info_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Ensure the window stays on top
        self.root.attributes('-topmost', True)

    def start_clicking(self):
        self.clicking = True
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.info_label.config(text="Clicking started. Move your mouse.")

        self.click_thread = threading.Thread(target=self.click_mouse)
        self.click_thread.start()

        self.root.after(120000, self.auto_stop)  # Automatically stop after 15 seconds

    def auto_stop(self):
        if self.clicking:
            self.stop_clicking()

    def stop_clicking(self):
        self.clicking = False
        self.stop_event.set()
        self.info_label.config(text="Clicking stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.click_thread.join()

    def click_mouse(self):
        while self.clicking and not self.stop_event.is_set():
            pyautogui.mouseDown()
            pyautogui.mouseUp()

if __name__ == "__main__":
    root = tk.Tk()
    app = RapidClickBot(root)
    root.mainloop()
