import cv2
#to enhace the accuracy of the model 
def resize_ara_num( image):
        try:
            width = 700
            height = 400
            dim = (width, height)
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            return image
        except Exception as e:
            print("Error occurred during resizing:", e)
            return None
    
def gray(image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray
        except Exception as e:
            print("Error occurred during conversion to grayscale:", e)
            return None

def increase_contrast( image):
        try:
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