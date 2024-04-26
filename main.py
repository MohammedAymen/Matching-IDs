import cv2
import pytesseract
from filters import gray,increase_contrast,resize_ara_num 
from CompareFace import CompareFace
from scanner import detect_id_card
from rotation import detect_orientation
class Comp:
    def __init__(self, image1_path, image2_path):
        pytesseract.pytesseract.tesseract_cmd = r'D:\my stuff\OCR\tesseract.exe'
        self.image1_path = image1_path
        self.image2_path = image2_path
    
    def extract_ara_num(self, image):
        try:
            image=detect_id_card(image)
            image=detect_orientation(image)
            image = resize_ara_num(image)
            h, w, ch = image.shape
            image = image[int(h / 1.8):int(h / 1.08), int(w / 2.8):int(w / 1)]
            copy = image
            count = 0
            while True:
                count += 1
                image = gray(image)
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
                image = increase_contrast(copy)
                if count > 1:
                    image = increase_contrast(image)
                if count == 3:
                    return "please re-capture the image"
                continue
        except Exception as e:
            print("Error occurred during image processing:", e)
            return None
        
    def Check(self, image1_path, image2_path):
        try:
            #image1 = cv2.imread(image1_path)
            #image2 = cv2.imread(image2_path)
            ara_num_res1 = self.extract_ara_num(image1_path)
            ara_num_res2 = self.extract_ara_num(image2_path)
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
                Match = CompareFace(image1_path, image2_path)
                if Match:
                    return True
            return False
        except Exception as e:
            print("Error occurred during check:", e)
            return None

image1_path = r"D:\final project face recognition\data set\system\6.jpg"
image2_path = r"D:\final project face recognition\data set\users captured\6.jpg"

comp_instance = Comp(image1_path, image2_path)

result = comp_instance.Check(image1_path, image2_path)

print("Result:", result)
