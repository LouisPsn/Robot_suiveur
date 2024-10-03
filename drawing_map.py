import cv2
import numpy as np
import math

# Création d'une image vide pour représenter la carte
map_image = np.ones((800,800, 3), dtype=np.uint8) * 255  # Fond blanc

# Position initiale du robot au centre de l'image (x, y)
current_position = (250, 250)  # Centre de la carte

# Simuler une fonction pour obtenir les données des capteurs
def get_sensor_data():
    # Simuler un déplacement avec une distance et un angle aléatoires (à remplacer par des données réelles)
    # Par exemple, à chaque itération, nous allons faire avancer le robot d'une certaine distance
    distance = np.random.randint(5, 15)  # Distance aléatoire entre 5 et 15 pixels
    angle = np.random.uniform(0, 2 * math.pi)  # Angle aléatoire entre 0 et 360 degrés
    return distance, angle

# Boucle principale pour suivre les déplacements du robot en temps réel
while True:
    # Récupérer les données simulées des capteurs (ou remplacer cette ligne par vos capteurs réels)
    distance, angle = get_sensor_data()

    # Calculer les changements en x et y basés sur la distance et l'angle
    dx = int(distance * math.cos(angle))
    dy = int(distance * math.sin(angle))

    # Nouvelle position du robot
    new_position = (current_position[0] + dx, current_position[1] + dy)

    # Tracer une ligne entre l'ancienne et la nouvelle position
    cv2.line(map_image, current_position, new_position, (0, 0, 255), 2)

    # Mettre à jour la position courante
    current_position = new_position

    # Afficher la carte avec le chemin mis à jour en temps réel
    cv2.imshow("Skyview Map", map_image)

    # Attendre 50ms pour simuler le temps réel (et permettre de quitter avec la touche 'q')
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Fermer toutes les fenêtres lorsque l'utilisateur quitte
cv2.destroyAllWindows()

# Enregistrer la carte finale comme image
cv2.imwrite('skyview_map.png', map_image)
def get_sensor_data():
    # Remplacez par la récupération des données réelles du capteur
    distance = read_distance_from_encoder()  # Lire la distance des encodeurs
    angle = read_angle_from_imu()            # Lire l'angle de l'IMU
    return distance, angle

