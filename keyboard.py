import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Keyboard layout (QWERTY)
keyboard = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
]

# Keyboard settings
key_width = 60
key_height = 60
key_margin = 5
keyboard_x = 50
keyboard_y = 100

# Track pressed key
pressed_key = None

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Draw keyboard
    for i, row in enumerate(keyboard):
        for j, key in enumerate(row):
            x = keyboard_x + j * (key_width + key_margin)
            y = keyboard_y + i * (key_height + key_margin)
            
            # Highlight if key is pressed
            color = (0, 255, 0) if pressed_key == key else (200, 200, 200)
            cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), color, -1)
            cv2.putText(frame, key, (x + 20, y + 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Hand detection
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger tip coordinates
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            
            # Draw finger tip
            cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)
            
            # Check key press
            pressed_key = None
            for i, row in enumerate(keyboard):
                for j, key in enumerate(row):
                    x = keyboard_x + j * (key_width + key_margin)
                    y = keyboard_y + i * (key_height + key_margin)
                    
                    if x < ix < x + key_width and y < iy < y + key_height:
                        pressed_key = key
                        break
    
    # Display pressed key
    if pressed_key:
        cv2.putText(frame, f"Pressed: {pressed_key}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Virtual Keyboard', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()