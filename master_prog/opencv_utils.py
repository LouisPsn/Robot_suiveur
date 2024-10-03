import cv2

def initVideoCapture(port:int) -> cv2.VideoCapture: 
    return cv2.VideoCapture(port)
