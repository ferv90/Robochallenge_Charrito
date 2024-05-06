# 8import WebcamModule as wM
# import DataCollectionModule as dcM
import KeyboardModule as kbM
# import MotorModule as mM
import cv2
from time import sleep

maxThrottle = 0.258
# motor = mM.Motor()

recStatus = 0
while True:
    keyVal = kbM.keyEvent()
    print("input:", keyVal)
    recording   = keyVal['recordctl']
    steering    = keyVal['steering']
    throttle    = keyVal['speed']*maxThrottle

    if recording == 1 and recStatus == 0:
         print('Recording Started ...')
         recStatus +=1
         sleep(0.300)

    if recStatus == 1:
        # img = wM.getImg(True,size=[240,120])
        print("Save data steering")
        # dcM.saveData(img,steering)

    if recording == 3 and recStatus == 1:
        print("Stop data record and save log file...")
        # dcM.saveLog()
        recStatus = 0

    # motor.move(throttle,-steering)
    cv2.waitKey(9)