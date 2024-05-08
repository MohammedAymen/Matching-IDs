from flask import Flask, request
import numpy as np
import cv2
from main import Comp 
from CompareFace import CompareFace
app = Flask(__name__)
 
 
@app.route("/", methods=["POST"])
def receive_images():
    images = []
    for image_file in request.files.getlist("images"):
 
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
 
        images.append(img)
       # print(img)
        print("image shape",img.shape)
    #["app", "personal", "system"]
    imageapp=images[0]
    imagePers=images[1]
    imageSystem=images[2]
    comp_instance = Comp(imageapp, imageSystem)
    result1= comp_instance.Check()
    result2 =CompareFace(imageSystem, imagePers)
    
    if result1 and result2:
        return "Allowed to register", 200
    return "Not allowed to register", 400
 
if __name__ == "__main__":
    app.run(debug=False)