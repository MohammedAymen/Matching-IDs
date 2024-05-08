from deepface import DeepFace
import cv2
#to implement face verification 
def CompareFace(image1, image2):
        try:
            result = DeepFace.verify(img1_path=image1, img2_path=image2, model_name="Facenet", detector_backend='fastmtcnn')
            if result['verified']:
               return True   
            else:
               return False
        except Exception as e:
            print("Error occurred during face comparison:", e)
            return None
      