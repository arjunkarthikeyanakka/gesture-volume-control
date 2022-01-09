
import mediapipe as mp
import cv2
import time
import handtrackermodule as htm

prevTime = 0
currTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while 1:
        # the following code will open up a new window that shows feed from webcam... , infinetely , to stop press stop running on top right..
        success, img = cap.read()
        img = detector.findHands(img,draw_landmarks=False)
        lmlist = detector.findPosition(img,draw_circle=True)
        if len(lmlist):
            print(lmlist[0])
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        # this will print frames per second on the coordinates (10,70) on the window
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3)

        cv2.imshow("Hand tracker", img)
        cv2.waitKey(1)