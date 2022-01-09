import cv2
import mediapipe as mp
import time  # to check the frame rate


print('setup complete good to go , the window opening is of size 600x480 px')


class handDetector():

    # initialisation
    def __init__(self, mode=False, maxhands=2,complexity = 1, detection_confidence=0.75, tracking_confidence=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.complexity = complexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxhands,self.complexity,self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img,draw_landmarks=True):
        # converting image to rgb image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # this will process the frame for us and give us the info
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
        # mpDraw.draw_landmarks(img,handLms) #this prints 21 points for us in the feed of the camera on each finger on each hand
        # mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) # this will show the connections between each point on a finger

        # now we get the info of each finger in a hand , like the id numbers and landmarks
        # for id, lm in enumerate(handLms.landmark):
        #     # print(id,lm) #this will give decimal values
        #     height, width, channels = img.shape
        #     cx, cy = int(lm.x * width), int(
        #         lm.y * height)  # is the position of the center , its an integer so we have to convert landmark in to int
        #     # this will print point number and coordinates.
        #     terminal_fodder = f"Co-ordinates of the point {id} in pixels are : {cx} and {cy}"
        #     # print(terminal_fodder)
        #     if id and id % 4 == 0:
        #         cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    def findPosition(self, img,fingerNumber=0,draw_circle=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[fingerNumber]
            for id, lm in enumerate(myHand.landmark):
                height, width, channels = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                lmList.append([id, cx, cy])
                #cv2.circle(img, (cx, cy), 13, (0, 255, 0), cv2.FILLED)
        return lmList


def main():
    prevTime = 0
    currTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while 1:
            # the following code will open up a new window that shows feed from webcam... , infinetely , to stop press stop running on top right..
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist):
            print(lmlist[0])
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

            # this will print frames per second on the coordinates (10,70) on the window
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 3)

        cv2.imshow("Hand tracker", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()