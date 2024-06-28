import cv2
import numpy as np

# Resize the image
def resize_image(image, width=700, height=400):
    try:
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return image
    except Exception as e:
        print("Error occurred during resizing:", e)
        return None

# Convert to grayscale
def convert_to_gray(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    except Exception as e:
        print("Error occurred during conversion to grayscale:", e)
        return None

# Increase contrast
def enhance_contrast(image):
    try:
        if len(image.shape) == 2:  # If image is already in grayscale
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(image)
            return cl
        else:  # If image has more than one channel
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            return final
    except Exception as e:
        print("Error occurred during contrast enhancement:", e)
        return None

# Apply Gaussian blur
def apply_gaussian_blur(image, kernel_size=(5, 5)):
    try:
        blurred = cv2.GaussianBlur(image, kernel_size, 0)
        return blurred
    except Exception as e:
        print("Error occurred during Gaussian blurring:", e)
        return None

# Adjust brightness and contrast
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    try:
        beta = brightness  # Brightness
        alpha = contrast / 127 + 1  # Contrast
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted
    except Exception as e:
        print("Error occurred during brightness/contrast adjustment:", e)
        return None

# Sharpen the image
def sharpen_image(image):
    try:
        kernel = np.array([[0, -1, 0], 
                           [-1, 5, -1], 
                           [0, -1, 0]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened
    except Exception as e:
        print("Error occurred during sharpening:", e)
        return None

# Preprocess the image
def preprocess_image(image):
    image = resize_image(image)
    image = apply_gaussian_blur(image)
    image = adjust_brightness_contrast(image, brightness=30, contrast=30)
    image = sharpen_image(image)
    return image


