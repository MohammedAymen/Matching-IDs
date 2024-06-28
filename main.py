import cv2
import pytesseract
from filters import preprocess_image,enhance_contrast,convert_to_gray
from CompareFace import CompareFace
from scanner import detect_id_card
#from rotation import detect_orientation
class Comp:
    def __init__(self, imageapp, imageSystem):
        #pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        pytesseract.pytesseract.tesseract_cmd = r'D:\my stuff\OCR\tesseract.exe'
        self.imageapp = imageapp
        self.imageSystem = imageSystem
    
    def extract_ara_num(self, image):
        try:
            image=detect_id_card(image)
            #image=detect_orientation(image)
            image = preprocess_image(image)
            h, w, ch = image.shape
            image = image[int(h / 1.8):int(h / 1.08), int(w / 2.8):int(w / 1)]
            copy = image
            count = 0
            while count < 3:
                count += 1
                image = convert_to_gray(image)
                _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                res = pytesseract.image_to_string(image, lang="ara_number_id").split()
                if res:
                    for i in res:
                        if 13 < len(i) < 15:
                            return i
                f_res = ""
                for i in range(1, len(res) + 1):
                    if i > 1:
                        f_res = res[len(res) - i] + f_res
                    else:
                        f_res += res[len(res) - i]
                    if len(f_res) == 14:
                        return f_res
                image = enhance_contrast(copy)
                if count > 1:
                    image = enhance_contrast(image)
                if count == 3:
                    return "please re-capture the image"
                continue
        except Exception as e:
            print("Error occurred during image processing:", e)
            return None
        
    def check(self):
        try:
            ara_num_res1 = self.extract_ara_num(self.imageapp)
            ara_num_res2 = self.extract_ara_num(self.imageSystem)
            if not ara_num_res1 or not ara_num_res2:
                print("Error: Unable to extract Arabic numbers from images.")
                return False
            
            arabic_to_english_map = {
                '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
            }

            english_number1 = ''.join(arabic_to_english_map[digit] for digit in ara_num_res1 if digit in arabic_to_english_map)
            english_number2 = ''.join(arabic_to_english_map[digit] for digit in ara_num_res2 if digit in arabic_to_english_map)
            print("ID one:", english_number1)
            print("ID two:", english_number2)
            
            if english_number1 and english_number1 == english_number2:
                Match = CompareFace(self.imageapp, self.imageSystem)
                if Match:
                    return True
            return False
        except Exception as e:
            print("Error occurred during check:", e)
            return None

