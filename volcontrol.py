import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp
import cv2
import handtrackermodule as htm
import numpy as np

wcam, hcam = 1024, 512
cap = cv2.VideoCapture(0)
cap.set(3, wcam)  # sets width of the window to 1024 px
cap.set(4, hcam)  # sets height of the window to 512 px

HandTracker = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#the below command will give the range of vol : (-63.5, 0.0)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

ptime = 0
bar = 400
vol = 0
volperc = 0
while 1:
    s, i = cap.read()
    i = HandTracker.findHands(i)
    lmlist = []
    lmlist = HandTracker.findPosition(i)
    if lmlist:
        x,y = int(lmlist[4][1]), int(lmlist[4][2])
        a,b = int(lmlist[8][1]), int(lmlist[8][2])
        midx , midy = (x+a)//2 , (y+b)//2
        cv2.circle(i, (x, y), 8, (0, 255, 0), cv2.FILLED)
        cv2.circle(i, (a, b), 8, (0, 255, 0), cv2.FILLED)
        cv2.line(i, (x, y), (a, b), (0, 0, 255), 3)
        length=math.hypot(x-a,y-b)
        #print(vol)
        #range of volume : 30 , 230
        vol = np.interp(length , [30,230],[minVol,maxVol])
        bar = np.interp(length , [30,230] , [400,150])
        volperc = np.interp(length,[30,230],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        if volperc==0 or volperc==100:
            cv2.circle(i, (midx, midy), 8, (0, 0, 0), cv2.FILLED)
        else:
            cv2.circle(i, (midx, midy), 8, (0, 255, 0), cv2.FILLED)
        #cv2.rectangle(i,(100,100),(150,300),(0,0,0),vol//2+1)
        cv2.rectangle(i,(50,150),(85,400),(0,255,0),2)
        cv2.putText(i, f'{int(volperc)}%', (50, 145), 2, cv2.FONT_HERSHEY_PLAIN, (0, 255, 0), 2)
        cv2.rectangle(i,(50,int(bar)),(85,400),(0,255,0),cv2.FILLED)


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(i, f'FPS:{int(fps)}', (50, 50), 3, cv2.FONT_HERSHEY_PLAIN, (0, 255, 0), 2)
    cv2.imshow("Gesture Volume Controlling", i)
    cv2.waitKey(1)
