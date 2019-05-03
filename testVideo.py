import cv2
import matplotlib.pyplot as plt 

path = "/media/mathieu/Nouveau nom/videos_bille/mes_cam_bille1_1.avi"
cap = cv2.VideoCapture(path)


length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
rate = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

print(length, width, height, rate)
# while(True):
#     ret, frame = cap.read()
#     nb_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
#     print(nb_frame)
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

cap.set(1, 10000)
ret, frame = cap.read()
cv2.imshow('frame', frame)
while True:
    ch = 0xFF & cv2.waitKey(1) # Wait for a second
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()