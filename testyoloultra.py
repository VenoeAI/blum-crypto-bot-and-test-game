from ultralytics import YOLO
from PIL import ImageGrab
import lap 

def main():
    model = YOLO('best.pt')
    img = ImageGrab.grab()
    result = model.track(source=img, show=True)


if __name__ == '__main__':
    main()