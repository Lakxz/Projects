import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# For smooth movement
prev_x, prev_y = 0, 0
smoothening = 5
prev_scroll_dist = 0

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                x, y = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, x, y))

            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get important landmarks
            x_index, y_index = lm_list[8][1], lm_list[8][2]
            x_thumb, y_thumb = lm_list[4][1], lm_list[4][2]
            x_ring, y_ring = lm_list[16][1], lm_list[16][2]
            x_middle, y_middle = lm_list[12][1], lm_list[12][2]

            # Move cursor
            screen_x = np.interp(x_index, [0, w], [0, screen_width])
            screen_y = np.interp(y_index, [0, h], [0, screen_height])
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Left Click (Index + Thumb)
            dist_thumb_index = math.hypot(x_thumb - x_index, y_thumb - y_index)
            if dist_thumb_index < 30:
                cv2.putText(frame, 'Left Click', (x_index, y_index - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                pyautogui.click()
                time.sleep(0.3)

            # Right Click (Ring + Thumb)
            dist_thumb_ring = math.hypot(x_thumb - x_ring, y_thumb - y_ring)
            if dist_thumb_ring < 30:
                cv2.putText(frame, 'Right Click', (x_index, y_index - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                pyautogui.rightClick()
                time.sleep(0.3)
                


            # Scroll (Middle + Index)
            scroll_dist = math.hypot(x_index - x_middle, y_index - y_middle)
            if scroll_dist > prev_scroll_dist + 10:
                pyautogui.scroll(-50)  # Scroll down
                cv2.putText(frame, 'Scrolling Down', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
            elif scroll_dist < prev_scroll_dist - 10:
                pyautogui.scroll(50)   # Scroll up
                cv2.putText(frame, 'Scrolling Up', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)
            prev_scroll_dist = scroll_dist

    # Show frame
    cv2.imshow("Virtual Mouse with Scroll", frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
