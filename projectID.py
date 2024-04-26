import pytesseract
import cv2
from deepface import DeepFace
#that for impliment the whole code on one file and without using rotation and detect_id 
#thats for testing  
class Comp:
    def __init__(self, image1, image2):
        pytesseract.pytesseract.tesseract_cmd = r'D:\my stuff\OCR\tesseract.exe'
        self.image1 = image1
        self.image2 = image2
    
    def extract_ara_num(self, image):
        try:
            image = self.resize_ara_num(image)
            h, w, ch = image.shape
            image = image[int(h / 1.8):int(h / 1.08), int(w / 2.8):int(w / 1)]
            copy = image
            ##############################
            count = 0
            # in the loop until reading the number
            
            while True:
                count += 1
                image = self.gray(image)
                _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                res = pytesseract.image_to_string(image, lang="ara_number_id").split()
                if res:
                    for i in res:
                        if 13 < len(i) < 15:
                            return i
                f_res = ""
                for i in range(1, len(res) + 1):
                    if i > 1:
                        temp = res[len(res) - i]
                        temp += f_res
                        f_res = temp
                    else:
                        f_res += res[len(res) - i]
                    if len(f_res) == 14:
                        return f_res
                image = self.increase_contrast(copy)
                if count > 1:
                    image = self.increase_contrast(image)
                if count == 3:
                    return "please re-capture the image"
                continue
        except Exception as e:
            print("Error occurred during image processing:", e)
            return None

    def resize_ara_num(self, image):
        try:
            width = 700
            height = 700
            dim = (width, height)
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            return image
        except Exception as e:
            print("Error occurred during resizing:", e)
            return None
    
    def gray(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray
        except Exception as e:
            print("Error occurred during conversion to grayscale:", e)
            return None
    
    def increase_contrast(self, image):
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
    
    def CompareFace(self, image1, image2):
        try:
            result = DeepFace.verify(img1_path=image1, img2_path=image2, model_name="Facenet", detector_backend='mtcnn')
            if result['verified']:
               return True   
            else:
               return False
        except Exception as e:
            print("Error occurred during face comparison:", e)
            return None
        
    def Check(self, image1, image2):
        try:
            ara_num_res1 = self.extract_ara_num(image1)
            ara_num_res2 = self.extract_ara_num(image2)
            if ara_num_res1 is None or ara_num_res2 is None:
                print("Error: Unable to extract Arabic numbers from images.")
                return None
            
            arabic_to_english_map = {
                '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
            }

            english_number1 = ''.join(arabic_to_english_map[digit] for digit in ara_num_res1 if digit in arabic_to_english_map)
            english_number2 = ''.join(arabic_to_english_map[digit] for digit in ara_num_res2 if digit in arabic_to_english_map)
            print("ID one",english_number1)
            print("ID two",english_number2)
            
            if english_number1 == english_number2:
                Match = self.CompareFace(image1, image2)
                if Match:
                    return True
            return False
        except Exception as e:
            print("Error occurred during check:", e)
            return None

image1_path = cv2.imread(r"D:\final project face recognition\data set\system\7.jpeg")
image2_path = cv2.imread(r"D:\final project face recognition\data set\users captured\7.jpeg")

comp_instance = Comp(image1_path, image2_path)

result = comp_instance.Check(image1_path, image2_path)

print("Result:", result)
