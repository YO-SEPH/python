import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=1
)

is_first = True
first_center_x, first_center_y, first_radius = None,None,None

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img_h, img_w, _ = img.shape

    img_result = img.copy()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img)

    mp_drawing.draw_landmarks(
        img_result,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_style.get_default_pose_landmarks_style()
    )

    if results.pose_landmarks:
        landmark = results.pose_landmarks.landmark

        left_ear_x = landmark[mp_pose.PoseLandmark.LEFT_EAR].x * img_w
        left_ear_y = landmark[mp_pose.PoseLandmark.LEFT_EAR].y * img_h

        right_ear_x = landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * img_w
        right_ear_y = landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * img_h

        center_x = int((left_ear_x + right_ear_x) / 2)
        center_y = int((left_ear_y + right_ear_y) / 2)

        radius = int((left_ear_x - right_ear_x) / 2)
        radius = max(radius, 10)

        if is_first:
            first_center_x = center_x
            first_center_y = center_y
            first_radius = int(radius * 2)

            is_first = False
        else:
            cv2.circle(img_result, center = (first_center_x, first_center_y), radius=first_radius, color=(255,255,255), thickness=2)
            color = (0,255,0)

            if center_x - radius < first_center_x - first_radius \
                or center_x + radius > first_center_x + first_radius:
                color = (0,0,255)

            cv2.circle(img_result, center=(center_x, center_y), radius=radius, color=color, thickness=2)

    cv2.imshow("Coach", cv2.flip(img_result,1))

    if cv2.waitKey(1) == ord('q'):
        break

pose.close()
cap.release()