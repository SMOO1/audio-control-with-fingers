import cv2
import math
import time
import win32api
import win32con
from cvzone.HandTrackingModule import HandDetector

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)  #points (tip of thumb and index finger) inputted into the length of a line segment formula to get the distance

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
distance_bar_color = (0, 255, 0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hands, img = detector.findHands(frame)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        thumb_tip = hand["lmList"][4]
        index_tip = hand["lmList"][8]

        #distance from thumb tip to index finger tip
        distance = calculate_distance(thumb_tip, index_tip)
        distance_percent = int((distance / 50) * 100)

        bar_height = int((1 - distance_percent / 100) * frame.shape[0])
        cv2.rectangle(frame, (0, bar_height), (30, frame.shape[0]), distance_bar_color, cv2.FILLED)

        #distance determines if hand is in a pinch or open pinch position
        #simulate volume increase and decrease key presses 
        if fingers[1] == 1 and fingers[2] == 1:
            if distance < 50:
                cv2.putText(img, "pinch", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, 0, 0)
                win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                cv2.putText(img, "expanded pinch", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                win32api.keybd_event(win32con.VK_VOLUME_UP, 0, 0, 0)
                win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP, 0)

    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()
