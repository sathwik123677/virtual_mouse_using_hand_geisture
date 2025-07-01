#virtual mouse 
import cv2
import numpy as np 
import pyautogui
import time
import math
import mediapipe as mp
import handtrackingmodule as htm
from pynput.mouse import Button, Controller
import random
mouse=Controller()
detector = htm.HandDetector()
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
#screen resolution
ptime = 0
def distance(p1,p2):
    dist = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    return dist
def get_angle(p1,p2,p3):
    a=np.array(p1)
    b=np.array(p2)
    c=np.array(p3)
    angle=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(angle*180/np.pi)
    if angle>180:
        angle=360-angle
    return angle
def move_mouse(indextip):
    if indextip is not None:
     indextip = list(indextip)
    else:
        print("No index tip detected")
        return  
    # print(indextip)
    x=int(indextip[0])
    y=int(indextip[1])
    print(x,y)
    screen_width, screen_height = pyautogui.size()
    x_screen = np.interp(x, (0, wCam), (0, screen_width))
    y_screen = np.interp(y, (0, hCam), (0, screen_height))
    pyautogui.moveTo(x_screen, y_screen, duration=0.1)
def is_left(lmlist,distancetip):
    if len(lmlist)!=0:
        indextip = lmlist[8][1:]
        thumbtip = lmlist[4][1:]
        distancetip = distance(indextip,thumbtip)
        angle=get_angle(lmlist[5][1:],lmlist[6][1:],lmlist[8][1:])
        angle2=get_angle(lmlist[9][1:],lmlist[10][1:],lmlist[12][1:])

        if angle2 > 90 and angle <50  and distancetip>50:
            return True            
    return False
def is_right(lmlist,distancetip):
    if len(lmlist)!=0:
        indextip = lmlist[8][1:]
        thumbtip = lmlist[4][1:]
        distancetip = distance(indextip,thumbtip)
        angle=get_angle(lmlist[5][1:],lmlist[6][1:],lmlist[8][1:])
        angle2=get_angle(lmlist[9][1:],lmlist[10][1:],lmlist[12][1:])
        if angle2 < 50 and angle >90  and distancetip>50:
            return True            
    return False
def is_doubleclick(lmlist,distancetip):
    if len(lmlist)!=0:
        indextip = lmlist[8][1:]
        thumbtip = lmlist[4][1:]
        distancetip = distance(indextip,thumbtip)
        angle=get_angle(lmlist[5][1:],lmlist[6][1:],lmlist[8][1:])
        angle2=get_angle(lmlist[9][1:],lmlist[10][1:],lmlist[12][1:])
        if angle2 < 50 and angle <50  and distancetip>50:
            return True            
    return False
def is_screeshot(lmlist,distancetip):
    if len(lmlist)!=0:
        indextip = lmlist[8][1:]
        thumbtip = lmlist[4][1:]
        distancetip = distance(indextip,thumbtip)
        angle=get_angle(lmlist[5][1:],lmlist[6][1:],lmlist[8][1:])
        angle2=get_angle(lmlist[9][1:],lmlist[10][1:],lmlist[12][1:])
        if angle2 < 50 and angle <50  and distancetip<50:
            return True            
    return False
def detect(img,lmlist):
    if len(lmlist)!=0:
        indextip = lmlist[8][1:]
        thumbtip = lmlist[4][1:]
        distancetip = distance(indextip,thumbtip)
        angle=get_angle(lmlist[5][1:],lmlist[6][1:],lmlist[8][1:])
        if distancetip < 50 and angle > 50:
            print("jello");
            move_mouse(indextip)
        elif is_left(lmlist,distancetip):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(img, "left click", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        elif is_right(lmlist,distancetip):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(img, "right click", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        elif is_doubleclick(lmlist,distancetip):
            pyautogui.doubleClick()
            cv2.putText(img, "double click", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            print("double click")
        elif is_screeshot(lmlist,distancetip):
            screenshot = pyautogui.screenshot()
            label = random.randint(1, 1000)
            screenshot.save(f'screenshot{label}.png')
            cv2.putText(img, "screenshot", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            print("Screenshot taken")
        # print(indextip)
        ##left click
        #index bend thumb and middle straight


while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img)
    detect(img,lmList);
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
