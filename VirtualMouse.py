import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy



wcam=640
hcam=480
pTime=0
frameR=100
clocX,clocY=0,0
plocX,plocY=0,0
smoothening=7
wScr,hScr=autopy.screen.size()
#print(wScr,hScr)

cap=cv2.VideoCapture(1)
cap.set(3,wcam)
cap.set(4,hcam)
detector=htm.HandDetector(maxHands=1)


while True:
    success, img=cap.read()
    img=detector.findhands(img)
    lmList,bbox=detector.findposition(img,draw=False)
    cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        #print(x1,y1,x2,y2)

        fingers=detector.fingersup()
        #print(fingers)

        if fingers[1]==1 and fingers[2]==0:

            x3=np.interp(x1,(frameR,wcam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hcam-frameR),(0,hScr))

            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening

            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY

        if fingers[1] == 1 and fingers[2] == 1:
            length,line=detector.finddistance(img,8,12)
            print(length)
            if length<40:
                cv2.circle(img, (line[4],line[5]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click()






    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.imshow("image",img)
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)
    cv2.waitKey(1)


