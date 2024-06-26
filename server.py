from flask import Flask, request, jsonify
import numpy as np
import cv2
from main import Comp
from CompareFace import CompareFace

app = Flask(_name_)

@app.route("/", methods=["GET", "POST"])
def receive_images():
    if request.method == "GET":
        return jsonify({
            "status": "success",
            "message": "Server is live"
        }), 200
    
    if request.method == "POST":
        try:
            images = []
            for image_file in request.files.getlist("images"):
                image_bytes = image_file.read()
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is None:
                    return jsonify({
                        "status": "error",
                        "message": "Failed to decode one or more images"
                    }), 400
                images.append(img)

            if len(images) != 3:
                return jsonify({
                    "status": "error",
                    "message": "Three images are required"
                }), 400
            
            imageapp = images[0]
            imagePers = images[1]
            imageSystem = images[2]

            comp_instance = Comp(imageapp, imageSystem)
            result1 = comp_instance.Check()
            result2 = CompareFace(imageSystem, imagePers)
            
            if result1 and result2:
                return jsonify({
                    "status": "success",
                    "message": "Allowed to register"
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Not allowed to register"
                }), 400
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000)
