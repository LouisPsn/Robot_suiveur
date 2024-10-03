import cv2
import numpy as np
import pypot.dynamixel

# Set up motors
ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')
dxl_io = pypot.dynamixel.DxlIO(ports[0])

def setup_motors():
    dxl_io.set_wheel_mode([1, 2])

def command_motors(vL, vR):
    dxl_io.set_moving_speed({1: -vL, 2: vR})
    
def detect_black_line(frame):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuillage pour détecter les pixels noirs
    # Tout ce qui est plus sombre que 50 est considéré comme noir
    _, mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

    # Optionnel : Appliquer des opérations morphologiques pour nettoyer l'image (érosion/dilatation)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Trouver les contours dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours sur l'image originale
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Afficher le masque avec la ligne noire isolée
    #cv2.imshow('Ligne noire détectée', mask)

    return mask, contours

# Utiliser la caméra pour capturer les images en direct
cap = cv2.VideoCapture(0)
saved_direction = [0, 0]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture de la caméra")
        break

    # Appeler la fonction de détection de ligne noire et des contours
    mask, contours = detect_black_line(frame)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, _, w, _ = cv2.boundingRect(c)

        center_x = x + w // 2
        _, width, _ = frame.shape

        if center_x > width/2 + width/4:
            command_motors(40, 300)
            saved_direction = [40, 300]
        elif center_x < width/4:
            command_motors(300, 40)
            saved_direction = [300, 40]
        else:
            command_motors(300, 300)
            saved_direction = [300, 300]
    else:
        if saved_direction[0] == saved_direction[1]:
            command_motors(0, 0)
        else:
            command_motors(saved_direction[0], saved_direction[1])

    # Afficher l'image originale avec les contours
    #cv2.imshow('Image originale avec contours', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
