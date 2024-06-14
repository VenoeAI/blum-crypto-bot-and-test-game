import cv2
import numpy as np
from ultralytics import YOLO
import mss
import pyautogui
import random
import time
import threading

# Load YOLOv8 model
model = YOLO('best.pt')

# Load classes (optional, depending on your use case)
classes = model.names

# Define the main region to capture
region = {'top': 74, 'left': 1379, 'width': 494, 'height': 966}

# Define the detection area
detection_region = region

# Define the clickable area
clickable_height = 100  # Adjust as needed
clickable_top = region['top'] + (region['height'] - clickable_height) // 2
clickable_region = {'top': clickable_top, 'left': region['left'], 'width': region['width'], 'height': clickable_height}

# Padding around detected objects to avoid accidental clicking
padding = 40  # Increased padding

# Function to detect objects in an image
def detect_objects(image):
    results = model(image)
    return results

# Function to perform a click at a specified position
def click(x, y):
    pyautogui.click(x, y)

# Function to generate random clicks within the specified region, avoiding detected objects
def generate_random_clicks(region, safe_areas, num_clicks):
    clicked_points = set()
    click_threads = []
    
    while len(click_threads) < num_clicks:
        x = random.randint(region['left'], region['left'] + region['width'] - 1)
        y = random.randint(region['top'], region['top'] + region['height'] - 1)
        
        # Check if the random point is near any safe area (with padding)
        safe = True
        for (x1, y1, x2, y2) in safe_areas:
            if x1 - padding <= x <= x2 + padding and y1 - padding <= y <= y2 + padding:
                safe = False
                break
        
        # Check if the point was already clicked in this round
        if safe and (x, y) not in clicked_points:
            clicked_points.add((x, y))
            thread = threading.Thread(target=click, args=(x, y))
            click_threads.append(thread)
    
    # Start all click threads
    for thread in click_threads:
        thread.start()
    
    # Wait for all threads to finish
    for thread in click_threads:
        thread.join()

# Capture the screen
with mss.mss() as sct:
    # Start timer
    start_time = time.time()
    max_duration = 2 * 60  # 2 minutes in seconds
    frame_time = 1 / 60  # Target frame time for 60 FPS

    while True:
        loop_start_time = time.time()
        
        # Capture the detection area
        detection_screenshot = sct.grab(detection_region)
        detection_image = np.array(detection_screenshot)

        # Convert from BGRA to BGR
        detection_image = cv2.cvtColor(detection_image, cv2.COLOR_BGRA2BGR)

        # Detect objects
        results = detect_objects(detection_image)

        # Extract safe areas from detected objects with padding
        safe_areas = []
        for result in results:
            boxes = result.boxes.xyxy.numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                safe_areas.append((x1 - padding, y1 - padding, x2 + padding, y2 + padding))
                # Debug: Print the coordinates of detected objects
                print(f"Detected object at: ({x1}, {y1}), ({x2}, {y2}) with padding")

        # Generate multiple random clicks within the clickable area, avoiding detected objects
        generate_random_clicks(clickable_region, safe_areas, num_clicks=10)

        # Calculate the time taken for this loop
        loop_end_time = time.time()
        elapsed_time = loop_end_time - loop_start_time

        # Sleep to maintain 60 FPS
        if elapsed_time < frame_time:
            time.sleep(frame_time - elapsed_time)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check if 2 minutes have passed
        total_elapsed_time = time.time() - start_time
        if total_elapsed_time > max_duration:
            break
