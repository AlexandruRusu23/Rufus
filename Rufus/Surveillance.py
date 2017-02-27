import numpy as np
import time
import datetime
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
numeOutput = 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(numeOutput,fourcc, 30.0, (640,480))

start_time = time.time()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        if ((time.time() - start_time) > 30):
            numeOutput = 'VIDEO' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.avi'
            out.release()
            out = cv2.VideoWriter(numeOutput,fourcc, 30.0, (640,480))
            start_time = time.time()

        out.write(frame)

        cv2.imshow(numeOutput,frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
