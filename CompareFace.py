from deepface import DeepFace


def CompareFace(image1, image2):

    try:
        result = DeepFace.verify(img1_path=image1, img2_path=image2, model_name="Facenet", detector_backend='opencv')
        return result['verified']
    except Exception as e:
        print("Error occurred during face comparison:", e)
        return False
    


