import cv2
import numpy as np
import dlib
from math import hypot
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2 )

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    faces = detector(gray)
    for face in faces:
        # print(face)
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()

        # cv2.rectangle(frame, (x,y), (x1,y1), (0,255,0), 2)

        landmarks = predictor(gray, face)

        # print(landmarks)
        # x = landmarks.part(36).x
        # y = landmarks.part(36).y
        # cv2.circle(frame, (x,y), 3, (0,0,255), 2)

        left_left_point = (landmarks.part(42).x, landmarks.part(42).y)
        left_right_point = (landmarks.part(45).x, landmarks.part(45).y)

        right_left_point = (landmarks.part(36).x, landmarks.part(36).y)
        right_right_point = (landmarks.part(39).x, landmarks.part(39).y)

        left_center_top = midpoint(landmarks.part(37), landmarks.part(38))
        left_center_bottom = midpoint(landmarks.part(41), landmarks.part(40))

        right_center_top = midpoint(landmarks.part(43), landmarks.part(43))
        right_center_bottom = midpoint(landmarks.part(47), landmarks.part(47))

        left_hor_line = cv2.line(frame, left_left_point, left_right_point, (0,0,255), 2)
        right_hor_line = cv2.line(frame, right_left_point, right_right_point, (0, 0, 255), 2)

        left_var_line = cv2.line(frame, left_center_top, left_center_bottom, (0,0,255), 2)
        right_var_line = cv2.line(frame, right_center_top, right_center_bottom, (0, 0, 255), 2)


        left_hor_lenght = hypot((left_left_point[0] - left_right_point[0]), (left_left_point[1] - left_right_point[1]))
        right_hor_lenght = hypot((right_left_point[0] - right_right_point[0]), (right_left_point[1] - right_right_point[1]))

        left_ver_line_lenght = hypot((left_center_top[0] - left_center_bottom[0]), (left_center_top[1] - left_center_bottom[1]))
        right_ver_line_lenght = hypot((right_center_top[0] - right_center_bottom[0]), (right_center_top[1] - right_center_bottom[1]))

        print(left_hor_lenght / left_ver_line_lenght)
        print("-------------------------------------")
        print(right_hor_lenght/ right_ver_line_lenght)


    cv2.imshow("Frame", cv2.flip(frame, 1))
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()