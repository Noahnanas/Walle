import cv2
import dlib
import imutils 
from scipy.spatial import distance as dist 
from imutils import face_utils 

import serial
import winsound

video_path = r"C:/Users/joker/Pictures/Camera Roll/testRec.mp4"  # Chemin de la vidéo
#cam = cv2.VideoCapture(video_path)
cam = cv2.VideoCapture(0)



def ratio_eye(eye): 
	y1 = dist.euclidean(eye[1], eye[5]) 
	y2 = dist.euclidean(eye[2], eye[4]) 

	x1 = dist.euclidean(eye[0], eye[3]) 

	EAR = (y1+y2) / x1 
	return EAR 

def brow_height(eyebrow, eye):
    heights = [abs(eyebrow[i][1] - eye[int(len(eye) / 2)][1]) for i in range(len(eyebrow))]
    return sum(heights) / len(heights)

# Variables 
blink_thresh = 0.5
succ_frame = 2
count_frame = 0
count_blink=0
active=False

# Eye landmarks 
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
(LB_start, LB_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
(RB_start, RB_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

detector = dlib.get_frontal_face_detector() 
predictor_path = "shape_predictor_68_face_landmarks.dat"
landmark_predict  = dlib.shape_predictor(predictor_path)

while 1: 
	_, frame = cam.read() 
	frame = imutils.resize(frame, width=640) 

	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

	faces = detector(img_gray) 
	for face in faces: 
		shape = landmark_predict(img_gray, face) 

		shape = face_utils.shape_to_np(shape) 

		lefteye = shape[L_start: L_end] 
		righteye = shape[R_start:R_end] 

		left_ratio = ratio_eye(lefteye)
		right_ratio = ratio_eye(righteye)
		avg = (left_ratio+right_ratio)/2
		print(avg)

		'''lefteyebrow = shape[LB_start:LB_end]
		righteyebrow = shape[RB_start:RB_end]
  
		left_brow_height = brow_height(lefteyebrow, lefteye)
		right_brow_height = brow_height(righteyebrow, righteye)
  
		normalized_left_brow = max(0, min(1, (left_brow_height - 5) / 20))
		normalized_right_brow = max(0, min(1, (right_brow_height - 5) / 20))
  
		cv2.putText(frame, f"L: {normalized_left_brow:.2f} R: {normalized_right_brow:.2f}", 
                    (450, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)'''
  
		if avg < blink_thresh: 
			count_frame += 1
			print(count_frame)
			if (count_frame >= succ_frame) and not (active): 
				count_blink+=1
					
				count_frame = 0
				active=True
		else:
			active=False
			count_frame = 0

		cv2.putText(frame, str(count_blink), (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 1) 

	cv2.imshow("Video", frame) 
	if cv2.waitKey(5) & 0xFF == ord('q'): 
		break

cam.release() 
cv2.destroyAllWindows() 
