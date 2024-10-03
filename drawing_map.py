import cv2
import numpy as np
import math
import time
import pypot.dynamixel

# Paramètres du robot
wheelDiameter = 5.2  # en cm
wheelDiameterSI = (wheelDiameter / 100)  # en mètres
wheelDistance = 14.5  # en cm
wheelDistanceSI = (wheelDistance / 100)  # en mètres
frequency = 5  # en Hz (fréquence de mise à jour)

# Création d'une image vide pour représenter la carte
map_image = np.ones((800, 800, 3), dtype=np.uint8) * 255  # Fond blanc

# Position initiale du robot au centre de l'image (x, y)
current_position = (400, 400)  # Centre de la carte (coordonnes dans une image 800x800)
worldTheta = 0  # Orientation initiale du robot (en radians)

# Fonction pour initialiser les moteurs Dynamixel
def init(motors):
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    print(ports)
    
    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    dxl_io.disable_torque(motors)
    dxl_io.set_wheel_mode(motors)
    return dxl_io

# Fonction pour convertir les vitesses des roues en vitesse linéaire et angulaire
def wheelSpeedConvertion(leftWheel, rightWheel):
    # Conversion des vitesses des roues en rad/s
    leftWheelRad = leftWheel * (math.pi / 180)
    rightWheelRad = rightWheel * (math.pi / 180)
    
    # Calcul de la vitesse linéaire et angulaire du robot
    linearSpeed = (wheelDiameterSI * (leftWheelRad + rightWheelRad)) / 2
    angularSpeed = (wheelDiameterSI * (rightWheelRad - leftWheelRad)) / wheelDistanceSI
    
    return linearSpeed, angularSpeed

# Fonction pour calculer les changements de position (x, y) et d'orientation (theta)
def speedToPosition(linearSpeed, angularSpeed, delta_time, theta):
    if angularSpeed == 0:  # Mouvement en ligne droite
        x = linearSpeed * delta_time
        y = 0
        new_theta = theta
    else:  # Mouvement en courbe
        radius = linearSpeed / angularSpeed
        x = radius * math.sin(angularSpeed * delta_time)
        y = radius * (1 - math.cos(angularSpeed * delta_time))
        new_theta = theta + angularSpeed * delta_time
    
    return x, y, new_theta

# IDs des moteurs (gauche et droite)
motorId = [1, 2]

# Initialiser les moteurs Dynamixel
dxl = init(motorId)

# Boucle principale pour suivre les déplacements du robot en temps réel
time_step = 1 / frequency  # Intervalle de temps entre chaque cycle

for i in range(1000):  # Vous pouvez ajuster la durée de la simulation
    # Récupérer les vitesses des roues (en degrés par seconde)
    leftSpeed, rightSpeed = dxl.get_present_speed(motorId)
    
    # Inverser la vitesse de la roue gauche si nécessaire
    leftSpeed = -leftSpeed
    
    # Convertir les vitesses des roues en vitesse linéaire et angulaire
    linearSpeed, angularSpeed = wheelSpeedConvertion(leftSpeed, rightSpeed)
    
    # Calculer les changements en x, y et theta
    dx, dy, dtheta = speedToPosition(linearSpeed, angularSpeed, time_step, worldTheta)
    
    # Mettre à jour la position globale du robot
    new_x = current_position[0] + int(dx * math.cos(worldTheta) - dy * math.sin(worldTheta))
    new_y = current_position[1] + int(dx * math.sin(worldTheta) + dy * math.cos(worldTheta))
    worldTheta += dtheta  # Mettre à jour l'orientation du robot
    
    new_position = (new_x, new_y)  # Nouvelle position du robot
    
    # Tracer une ligne entre l'ancienne et la nouvelle position sur la carte
    cv2.line(map_image, current_position, new_position, (0, 0, 255), 2)
    
    # Mettre à jour la position courante
    current_position = new_position

    # Afficher la carte avec le chemin mis à jour en temps réel
    cv2.imshow("Skyview Map", map_image)

    # Attendre un court délai pour simuler le temps réel
    if cv2.waitKey(int(time_step * 1000)) & 0xFF == ord('q'):
        break

# Fermer toutes les fenêtres lorsque l'utilisateur quitte
cv2.destroyAllWindows()

# Enregistrer la carte finale comme image
cv2.imwrite('skyview_map.png', map_image)
