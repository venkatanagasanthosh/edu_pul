import cv2
import face_recognition
import numpy as np
import base64

def encode_face(image_data):
    """Convert base64 image to face encoding"""
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    face_encodings = face_recognition.face_encodings(image)

    return face_encodings[0] if face_encodings else None

def compare_faces(stored_encoding, input_encoding):
    """Compare stored face encoding with input face encoding"""
    return face_recognition.compare_faces([stored_encoding], input_encoding)[0]
