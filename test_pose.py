import cv2
import mediapipe as mp

# Initialisation de MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Capture vidéo (remplace 'video.mp4' par le chemin de ta vidéo)
video_path = "testvid.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Conversion en RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape  # Dimensions de l'image

    # Dessiner les points du Face Mesh
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)  # Petit point vert

    # Affichage de la vidéo
    cv2.imshow("Face Mesh", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Appuie sur Échap pour quitter
        break

cap.release()
cv2.destroyAllWindows()
