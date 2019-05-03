import cv2
<<<<<<< HEAD
import matplotlib.pyplot as plt

path = "/home/fabouzz/Vidéos/"
videoName = 'test_cam6.avi'
cap = cv2.VideoCapture(path + videoName)

fps = cap.get(cv2.CAP_PROP_FPS)
frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
videoLength = frameCount / fps
print('Video length : {} s'.format(videoLength))
userTime = input('Choose video time (s) : ')

# while(True):
# Capture frame-by-frame
cap.set(cv2.CAP_PROP_POS_MSEC, int(userTime)*1000)
ret, frame = cap.read()

# Our operations on the frame come here
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the resulting frame
cv2.imshow('frame', gray)
cv2.waitKey(0)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break

# When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()
=======
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
>>>>>>> 2bdc20a6af37c348185332444f6ed6e9ac2fa088
