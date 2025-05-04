import time
import cv2
from picamera2 import Picamera2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=False)

# Camera init
screen_width, screen_height = 1280, 960 
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (screen_width, screen_height)})
picam2.configure(preview_config)
picam2.start()

#globale variables
last_frame = None
last_results = None
head_tilt_history=[0]*10
x_position_history = [0]*5
y_position_history = [0]*5

def gen_frames():
    global last_frame, last_results
    while True:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        results = face_mesh.process(frame)
        last_frame = frame
        last_results = results
        h, w, _ = frame.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        frame_process()
        time.sleep(0.03)


def frame_process():
    global last_frame, last_results
    x_position_history.pop(0)
    y_position_history.pop(0)
    head_tilt_history.pop(0)
    if last_results.multi_face_landmarks:
        face_landmarks = last_results.multi_face_landmarks[0]
        L_eye_bottom = face_landmarks.landmark[145] 
        R_eye_bottom = face_landmarks.landmark[374] 
        nose_tip = face_landmarks.landmark[1]  

        # position
        x_position_history.append(nose_tip.x)
        y_position_history.append(nose_tip.y)

        # head angle
        dx = R_eye_bottom.x - L_eye_bottom.x
        dy = R_eye_bottom.y - L_eye_bottom.y
        angle = np.arctan2(dy, dx)
        head_tilt_history.append((angle / (np.pi / 4) + 1) / 2)
    else:
        return None
    
def get_head_factor():
    x_position= round(sum(x_position_history) / len(x_position_history),2)
    y_position= round(sum(y_position_history) / len(y_position_history),2)
    head_tilt = round(sum(head_tilt_history) / len(head_tilt_history),2)
    return [x_position, y_position, head_tilt,len(head_tilt_history)]