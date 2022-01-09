import cv2
import mediapipe as mp
import time  # to check the frame rate
print('setup complete good to go')

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0


while 1:
    #the following code will open up a new window that shows feed from webcam... , infinetely , to stop press stop running on top right..
    success, img = cap.read()
    #converting image to rgb image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB) #this will process the frame for us and give us the info
    #now we have to extract the information of multiple hands
    #print(results.multi_hand_landmarks)  #this statement is to check whether there is actually any hand in front of the camera it shows the coordinates else just prints None.

    #for a hand there are 21 points
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #mpDraw.draw_landmarks(img,handLms) #this prints 21 points for us in the feed of the camera on each finger on each hand
            #mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) # this will show the connections between each point on a finger

            #now we get the info of each finger in a hand , like the id numbers and landmarks
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm) #this will give decimal values
                height , width , channels = img.shape
                cx, cy = int(lm.x*width) , int(lm.y*height)  #is the position of the center , its an integer so we have to convert landmark in to int
                 #this will print point number and coordinates.
                terminal_fodder = f"Co-ordinates of the point {id} in pixels are : {cx} and {cy}"
                #print(terminal_fodder)
                if id and id%4==0:
                    cv2.circle(img,(cx,cy),12,(0,255,0),cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime

    #this will print frames per second on the coordinates (10,70) on the window
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_DUPLEX,3,(0,0,0),3)

    cv2.imshow("Hand tracker", img)
    cv2.waitKey(1)
    
    #now we have to detect the hand in the web cam.

