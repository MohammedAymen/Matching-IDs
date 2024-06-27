import cv2
import gc

def resize_ara_num(image):
    try:
        width, height = 700, 400
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image
    except Exception as e:
        print("Error occurred during resizing:", e)
        return None

def gray(image):
    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image
    except Exception as e:
        print("Error occurred during conversion to grayscale:", e)
        return None

def increase_contrast(image):
    try:
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_image)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return final_image
    except Exception as e:
        print("Error occurred during contrast enhancement:", e)
        return None
    finally:
        gc.collect()  # Force garbage collection to free up memory
