import cv2
import pytesseract
import gc
from filters import gray, increase_contrast, resize_ara_num 
from CompareFace import CompareFace
from scanner import detect_id_card

class Comp:
    def __init__(self, imageapp, imageSystem):
        pytesseract.pytesseract.tesseract_cmd = r'D:\my stuff\OCR\tesseract.exe'
        self.imageapp = imageapp
        self.imageSystem = imageSystem
    
    def extract_ara_num(self, image):
        try:
            image = detect_id_card(image)
            image = resize_ara_num(image)
            h, w, ch = image.shape
            image = image[int(h / 1.8):int(h / 1.08), int(w / 2.8):int(w / 1)]
            copy = image
            count = 0
            while count < 3:
                count += 1
                gray_image = gray(image)
                _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                res = pytesseract.image_to_string(binary_image, lang="ara_number_id").split()
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
                image = increase_contrast(copy if count == 1 else image)
            return "please re-capture the image"
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
            
            if english_number1 == english_number2:
                match = CompareFace(self.imageapp, self.imageSystem)
                return match
            return False
        except Exception as e:
            print("Error occurred during check:", e)
            return None

        finally:
            gc.collect()  # Force garbage collection to free up memory
