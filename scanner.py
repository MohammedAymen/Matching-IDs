import cv2
import imutils
from transform import four_point_transform

#that function to detect id card and reshape the image into rounded the id 
def detect_id_card(image_path):
        image = cv2.imread(image_path)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 150, 200)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            #print("No ID card contour found in the image.")
            return image

        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
        newimg = cv2.resize(warped, (1000, 630))
        return newimg
