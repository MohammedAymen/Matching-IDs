import re
import cv2
import pytesseract
# that function to detect if the image rotated or not if rotated it fix it 
def detect_orientation(image):
        try:
           osd = pytesseract.image_to_osd(image)
           if osd is not None:
              angle_match = re.search(r'(?<=Rotate: )\d+', osd)
              if angle_match:
                  angle = angle_match.group(0)
                  script_match = re.search(r'(?<=Script: )\d+', osd)
                  if script_match:
                      script = script_match.group(0)
                  else:
                      script = None
                  #print("Angle:", angle)
                  #print("Script:", script)

                # Rotate the image if necessary
                  if angle != '0':
                    # Perform rotation
                     if angle == '90':
                        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                     elif angle == '180':
                        image = cv2.rotate(image, cv2.ROTATE_180)
                     elif angle == '270':
                        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

           return image
        except Exception as e:
           print("Error occurred during orientation detection:", e)
           return image
  