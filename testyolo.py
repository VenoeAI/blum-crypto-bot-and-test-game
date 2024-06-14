import cv2
import numpy as np
from ultralytics import YOLO
import mss

# Load YOLOv8 model
model = YOLO('best.pt')

# Load classes (optional, depending on your use case)
# If your YOLOv8 model is trained on a custom dataset, ensure you have the correct class names
classes = model.names

# Generate random colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Function to detect objects in an image
def detect_objects(image):
    results = model(image)
    return results

# Function to draw bounding boxes on the image
def draw_boxes(image, results):
    for result in results:
        boxes = result.boxes.xyxy.numpy()  # Bounding box coordinates
        confidences = result.boxes.conf.numpy()  # Confidence scores
        class_ids = result.boxes.cls.numpy().astype(int)  # Class IDs
        
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            x, y, x2, y2 = map(int, box)
            label = f"{classes[class_id]}: {confidence:.2f}"
            color = colors[class_id]
            cv2.rectangle(image, (x, y), (x2, y2), color, 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

# Capture the screen
with mss.mss() as sct:
    # Specify the part of the screen to capture (here, it captures the entire screen)
    monitor = sct.monitors[1]  # For the primary monitor
    
    # Create the window once
    cv2.namedWindow('Detected Objects', cv2.WINDOW_NORMAL)

    while True:
        # Capture the screen
        screenshot = sct.grab(monitor)
        image = np.array(screenshot)

        # Convert from BGRA to BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Detect objects
        results = detect_objects(image)

        # Draw bounding boxes
        image_with_boxes = draw_boxes(image, results)

        # Display the result in the same window
        cv2.imshow('Detected Objects', image_with_boxes)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the window
    cv2.destroyAllWindows()
