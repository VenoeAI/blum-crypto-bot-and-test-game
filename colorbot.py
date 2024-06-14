import pyautogui
import time

def find_color_line(colors, region):
    # Capture a thin line of pixels at the specified height
    line = pyautogui.screenshot(region=(region[0], region[1], region[2], 1))
    pixels = line.load()
    # Iterate through pixels in the line to find the color
    for x in range(line.width):
        pixel_color = pixels[x, 0][:3]  # Get RGB values of the pixel
        if pixel_color in colors:
            return x + region[0]  # Adjust x coordinate to global screen coordinate
    return -1

def click_on_color(colors, region):
    start_time = time.time()
    while time.time() - start_time < 30:  # Timeout after 30 seconds
        # Find the position of the color on the line
        x_pos = find_color_line(colors, region)
        if x_pos != -1:
            # Click on the found position
            pyautogui.click(x_pos, region[1] + region[3] // 2)  # Click in the center of the screen region
            time.sleep(0.5)  # Add a small delay to prevent rapid clicking
        time.sleep(0.1)  # Adjust this delay as necessary

# Example usage:
if __name__ == "__main__":
    # Specify the colors to monitor (RGB format)
    colors_to_monitor = [
        (230, 253, 151),  # RGB color (230, 253, 151)
        (201, 250, 24),   # RGB color (201, 250, 24)
        (227, 255, 134)   # RGB color (227, 255, 134)
    ]

    # Specify the screen region (top, left, width, height)
    region = (42, 1393, 495, 1026)  # Example: 100 pixels from top-left, 800 width, 600 height

    # Start monitoring and clicking on the specified colors
    click_on_color(colors_to_monitor, region)
