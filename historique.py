import cv2
import mediapipe as mp
import time
import serial

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
hand_points = []
is_set_open = False
is_set_close = False
arduino = serial.Serial('COM6', 9600)

def get_distance(point1, point2):
    return int(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5)

def get_distances(points, max_values=[1, 1, 1, 1, 1], min_values=[0, 0, 0, 0, 0]):
    thumb_base = points[2][1:]
    thumb_end = points[4][1:]
    thumb_distance = get_distance(thumb_base, thumb_end)
    thumb_ratio = thumb_distance / (max_values[0] - min_values[0])

    index_base = points[5][1:]
    index_end = points[8][1:]
    index_distance = get_distance(index_base, index_end)
    index_ratio = index_distance / (max_values[1] - min_values[1])

    middle_base = points[9][1:]
    middle_end = points[12][1:]
    middle_distance = get_distance(middle_base, middle_end)
    middle_ratio = middle_distance / (max_values[2] - min_values[2])

    ring_base = points[13][1:]
    ring_end = points[16][1:]
    ring_distance = get_distance(ring_base, ring_end)
    ring_ratio = ring_distance / (max_values[3] - min_values[3])

    pinky_base = points[17][1:]
    pinky_end = points[20][1:]
    pinky_distance = get_distance(pinky_base, pinky_end)
    pinky_ratio = pinky_distance / (max_values[4] - min_values[4])

    return thumb_distance, index_distance, middle_distance, ring_distance, pinky_distance, thumb_ratio, index_ratio, middle_ratio, ring_ratio, pinky_ratio

def set_open(distances):
    thumb, index, middle, ring, pinky = distances
    return thumb, index, middle, ring, pinky

def set_close(distances):
    thumb, index, middle, ring, pinky = distances
    return thumb, index, middle, ring, pinky

def send_data_by_COM(data_thumb, data_index, data_middle, data_ring, data_pinky):
    message = b'*%03d$%03d$%03d$%03d$%03d$*' % (1, data_index, data_middle, data_ring, data_pinky)
    arduino.write(message)
    time.sleep(0.05)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

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

    if len(hand_points) > 0:
        if is_set_open and is_set_close:
            t_d, i_d, m_d, r_d, p_d, thumb_ratio, index_ratio, middle_ratio, ring_ratio, pinky_ratio = get_distances(hand_points[0], [t_open, i_open, m_open, r_open, p_open], [t_close, i_close, m_close, r_close, p_close])
            send_data_by_COM(int(thumb_ratio * 90), int(index_ratio * 90), int(middle_ratio * 90), int(ring_ratio * 90), int(pinky_ratio * 90))
        else:
            t_d, i_d, m_d, r_d, p_d, thumb_ratio, index_ratio, middle_ratio, ring_ratio, pinky_ratio = get_distances(hand_points[0])

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('o'):
        t_open, i_open, m_open, r_open, p_open = set_open([t_d, i_d, m_d, r_d, p_d])
        is_set_open = True
    if key == ord('c'):
        t_close, i_close, m_close, r_close, p_close = set_close([t_d, i_d, m_d, r_d, p_d])
        is_set_close = True
