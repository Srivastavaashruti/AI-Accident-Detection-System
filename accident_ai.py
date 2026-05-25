import cv2
import numpy as np
import os

def detect_accident(image_path):

    print(" Checking:", image_path)

    if not os.path.exists(image_path):
        return "No Image Found", "Low"

    #  TRY BOTH METHODS
    img = cv2.imread(image_path)

    if img is None:
        print(" cv2.imread failed, trying imdecode...")

        try:
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        except:
            return "No Image Found", "Low"

    if img is None:
        return "No Image Found", "Low"

    print(" Image loaded")

    img = cv2.resize(img, (500, 500))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    edge_pixels = np.sum(edges > 0)

    print("Edges:", edge_pixels)

    if edge_pixels > 50000:
        return "Accident Detected", "High"
    elif edge_pixels > 25000:
        return " Possible Accident", "Medium"
    else:
        return "No Accident", "Low"
