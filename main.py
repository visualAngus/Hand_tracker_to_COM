import cv2
import mediapipe as mp
import time
import serial

# Initialisation de la caméra
cap = cv2.VideoCapture(0)

# Initialisation de la détection des points de la main
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

hand_points = []
is_set_open = False
is_set_close = False
arduino = serial.Serial('COM4', 9600)

def get_distance(point1, point2):
    """
    Calcule la distance entre deux points.
    
    Args:
        point1 (tuple): Coordonnées du premier point.
        point2 (tuple): Coordonnées du deuxième point.
    Returns:
        int: La distance entre les deux points.
    """
    return int(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5)

def gestion_doigts(point_id, id_doigt, base, min_values, max_values):
    end = points[point_id][1:]
    distance = get_distance(base, end)
    ratio = (distance - min_values[id_doigt]) / (max_values[id_doigt] - min_values[id_doigt])
    if ratio < 0:
        min_values[id_doigt] = distance - 1
        ratio = (distance - min_values[id_doigt]) / (max_values[id_doigt] - min_values[id_doigt])
    if ratio > 1:
        max_values[id_doigt] = distance + 1
        ratio = (distance - min_values[id_doigt]) / (max_values[id_doigt] - min_values[id_doigt])

    return distance, ratio, min_values, max_values


def get_distances(points, max_values=[1, 1, 1, 1, 1], min_values=[0, 0, 0, 0, 0]):
    """
    Calcule la distance entre la base et le bout de chaque doigts.

    Args:
        points (list): Liste des diff points de la main.
        max_values (list, optional): La distance maximal pour chaque distances calculées.
        min_values (list, optional): La distance minimal pour chaque distances calculées.

    Returns:
        tuple: Un tuple contenant les distances et les ratios de chaque doigts.
    """
    base = points[0][1:]
    distance = []
    ratio = []
    id_point = [4, 8, 12, 16, 20]
    for i in range(5):
        tmp_dist, ra, min_values, max_values = gestion_doigts(id_point[i], i, base, min_values, max_values)
        distance.append(tmp_dist)
        ratio.append(ra)
    return distance[0], distance[1], distance[2], distance[3], distance[4], ratio[0], ratio[1], ratio[2], ratio[3], ratio[4], min_values, max_values
    
def set_open(distances):
    """
    Définir les distances des doigts ouverts.
    Args:
        distances (list): Liste des distances des doigts.
    Returns:
        tuple: Les distances des doigts ouverts.
    """
    thumb, index, middle, ring, pinky = distances
    return thumb, index, middle, ring, pinky

def set_close(distances):
    """
    Définir les distances des doigts fermés.
    Args:
        distances (list): Liste des distances des doigts.
    Returns:
        tuple: Les distances des doigts fermés.
    """
    thumb, index, middle, ring, pinky = distances
    return thumb, index, middle, ring, pinky

def send_data_by_COM(data_thumb, data_index, data_middle, data_ring, data_pinky):
    """
    Envoyer les données par le port COM.
    Args:
        data_thumb (int): La distance du pouce.
        data_index (int): La distance de l'index.
        data_middle (int): La distance du majeur.
        data_ring (int): La distance de l'annulaire.
        data_pinky (int): La distance de l'auriculaire.
    """
    # Ajout des données et formatage du message
    message = b'*%03d$%03d$%03d$%03d$%03d$*' % (data_thumb, data_index, data_middle, data_ring, data_pinky)
    # Envoi du message
    # print(message)
    try:
        arduino.write(message)
    except:
        print("Erreur lors de l'envoi des données")
    time.sleep(0.05)

while True:
    # Lecture de l'image
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # Dessiner les points de la main
    if results.multi_hand_landmarks:
        hand_points = []
        for handLms in results.multi_hand_landmarks:
            points = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                points.append((id, cx, cy))
            hand_points.append(points)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Calculer les distances et les ratios
    if len(hand_points) > 0:
        if is_set_open and is_set_close:
            t_d, i_d, m_d, r_d, p_d, thumb_ratio, index_ratio, middle_ratio, ring_ratio, pinky_ratio,min_value,max_value = get_distances(hand_points[0], [t_open, i_open, m_open, r_open, p_open], [t_close, i_close, m_close, r_close, p_close])
            t_open, i_open, m_open, r_open, p_open = max_value
            t_close, i_close, m_close, r_close, p_close = min_value
            send_data_by_COM(int(thumb_ratio * 180), int(index_ratio * 180), int(middle_ratio * 180), int(ring_ratio * 180), int(pinky_ratio * 180))
        else:
            t_d, i_d, m_d, r_d, p_d, thumb_ratio, index_ratio, middle_ratio, ring_ratio, pinky_ratio,_,_ = get_distances(hand_points[0])
    # Afficher l'image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('o'):
        # Définir les distances des doigts ouverts
        t_open, i_open, m_open, r_open, p_open = set_open([t_d, i_d, m_d, r_d, p_d])
        is_set_open = True
    if key == ord('c'):
        # Définir les distances des doigts fermés
        t_close, i_close, m_close, r_close, p_close = set_close([t_d, i_d, m_d, r_d, p_d])
        is_set_close = True
