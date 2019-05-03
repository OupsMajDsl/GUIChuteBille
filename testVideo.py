import cv2
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
