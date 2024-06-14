import pyautogui
import cv2
import numpy as np
import time
import keyboard
import os

def capture_screen_region(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def load_templates(template_folder):
    templates = []
    for filename in os.listdir(template_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            template = cv2.imread(os.path.join(template_folder, filename))
            templates.append((template, filename))
    return templates

def average_color(image):
    return np.mean(image, axis=(0, 1))

def is_template_within_bounds(region, template):
    return region.shape[0] >= template.shape[0] and region.shape[1] >= template.shape[1]

def is_greyscale(color):
    return np.allclose(color[0], color[1], atol=10) and np.allclose(color[1], color[2], atol=10)

def find_templates(image, templates, avoidance_templates, confidence_threshold=0.9):
    detected_points = []
    for template, _ in templates:
        if not is_template_within_bounds(image, template):
            continue

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confidence_threshold)
        for pt in zip(*loc[::-1]):
            h, w = template.shape[:2]
            detected_region = image[pt[1]:pt[1] + h, pt[0]:pt[0] + w]
            if is_greyscale(average_color(detected_region)):
                continue
            if np.allclose(average_color(detected_region), average_color(template), atol=30):
                # Check against avoidance templates
                avoid = False
                for avoid_template, _ in avoidance_templates:
                    if not is_template_within_bounds(detected_region, avoid_template):
                        continue

                    avoid_res = cv2.matchTemplate(detected_region, avoid_template, cv2.TM_CCOEFF_NORMED)
                    if np.any(avoid_res >= confidence_threshold):
                        avoid = True
                        break
                if not avoid:
                    detected_points.append(pt)
    return detected_points

def click_points(points, region):
    for point in points:
        x = point[0] + region[0]
        y = point[1] + region[1]
        print(f"Clicking at ({x}, {y})")
        pyautogui.click(x, y)

def monitor_and_click(region, templates, avoidance_templates, confidence_threshold=0.9, interval=0.1):
    start_time = time.time()
    
    while True:
        # Check for time limit
        if time.time() - start_time > 60:
            print("Time limit reached. Exiting...")
            break

        # Check for key press
        if keyboard.is_pressed('q'):
            print("Key 'q' pressed. Exiting...")
            break

        screenshot = capture_screen_region(region)
        detected_points = find_templates(screenshot, templates, avoidance_templates, confidence_threshold)
        if detected_points:
            print(f"Detected points: {detected_points}")
            click_points(detected_points, region)

        time.sleep(interval)
def main():
    # Define the screen region to monitor (left, top, width, height)
    region = (1393, 42, 495, 1026)

    # Define the folder containing the template images
    template_folder = 'templates'

    # Define the folder containing the avoidance images
    avoidance_folder = 'avoidance'

    # Load the templates from the specified folder
    templates = load_templates(template_folder)
    avoidance_templates = load_templates(avoidance_folder)

    # Start the monitoring and clicking process
    monitor_and_click(region, templates, avoidance_templates)

if __name__ == "__main__":
    main()
