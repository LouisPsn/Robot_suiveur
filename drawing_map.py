import pypot.dynamixel
import math
import time
import matplotlib.pyplot as plt

# Paramètres du robot
wheelDiameter = 5.2  # en cm
wheelDiameterSI = (wheelDiameter / 100)  # en mètres
wheelDistance = 14.5  # en cm
wheelDistanceSI = (wheelDistance / 100)  # en mètres
frequency = 5  # en Hz (fréquence de mise à jour)

# Initialiser matplotlib pour tracer en temps réel
plt.ion()  # Mode interactif pour mise à jour en temps réel
fig, ax = plt.subplots()
ax.set_aspect('equal')
line, = ax.plot([], [], 'b-', label="Path")  # Tracer le chemin
arrow = ax.arrow(0, 0, 0.1, 0.1, head_width=0.05, head_length=0.1, fc='r', ec='r')

# Fonction pour initialiser les moteurs Dynamixel
def init(motors: list):
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
    leftWheelRad = leftWheel * (math.pi / 180)
    rightWheelRad = rightWheel * (math.pi / 180)
    linearSpeed = (wheelDiameterSI * (leftWheelRad + rightWheelRad)) / 2
    angularSpeed = (wheelDiameterSI * (rightWheelRad - leftWheelRad)) / wheelDistanceSI
    return linearSpeed, angularSpeed

# Fonction pour calculer les changements de position (x, y) et d'orientation (theta)
def speedToDelta(linearSpeed, angularSpeed, time, worldTeta):
    if angularSpeed == 0:  # Mouvement en ligne droite
        x = linearSpeed * time * math.cos(worldTeta)
        y = linearSpeed * time * math.sin(worldTeta)
        return x, y, 0
    else:  # Mouvement en courbe
        teta = angularSpeed * time
        x = (linearSpeed * time) * math.cos(worldTeta + angularSpeed * time)
        y = (linearSpeed * time) * math.sin(worldTeta + angularSpeed * time)
        return x, y, teta

# IDs des moteurs (gauche et droite)
motorId = [1, 2]

# Initialiser les moteurs Dynamixel
dxl = init(motorId)

# Variables de position et orientation du robot
worldX = 0
worldY = 0
worldTeta = 0

# Initialisation pour le traçage du chemin
positions_x = [worldX]
positions_y = [worldY]

# Boucle principale pour suivre les déplacements du robot en temps réel
for i in range(1000):
    # Récupérer les vitesses des roues (en degrés par seconde)
    leftSpeed, rightSpeed = dxl.get_present_speed([1, 2])
    
    # Inverser la vitesse de la roue gauche si nécessaire
    leftSpeed = -leftSpeed
    
    # Convertir les vitesses des roues en vitesse linéaire et angulaire
    linearSpeed, angularSpeed = wheelSpeedConvertion(leftSpeed, rightSpeed)
    
    # Calculer les changements en x, y et theta
    dx, dy, dtheta = speedToDelta(linearSpeed, angularSpeed, 1 / frequency, worldTeta)
    
    # Mettre à jour la position globale du robot
    worldX += dx
    worldY += dy
    worldTeta += dtheta  # Mettre à jour l'orientation du robot

    # Ajouter les nouvelles coordonnées à la liste
    positions_x.append(worldX)
    positions_y.append(worldY)
    
    # Mettre à jour le graphique
    line.set_data(positions_x, positions_y)  # Tracer le chemin
    arrow.remove()  # Supprimer l'ancienne flèche
    arrow = ax.arrow(worldX, worldY, 0.1 * math.cos(worldTeta), 0.1 * math.sin(worldTeta), 
                     head_width=0.05, head_length=0.1, fc='r', ec='r')  # Flèche pour direction
    
    # Ajuster les limites du graphique
    ax.relim()
    ax.autoscale_view()
    
    # Dessiner les changements
    plt.draw()
    plt.pause(1 / frequency)  # Pause pour laisser le temps à matplotlib d'afficher

# Afficher le graphique final
plt.ioff()  # Désactiver le mode interactif
plt.show()  # Afficher le graphique
