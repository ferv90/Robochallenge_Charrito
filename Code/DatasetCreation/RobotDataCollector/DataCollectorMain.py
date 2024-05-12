# import WebcamModule as wM
# import DataCollectionModule as dcM
import KeyboardGameModule as kbM
import MotorModule as robot
import cv2
from time import sleep

maxThrottle = 0.258
motors = robot.Motors(12,16,19,13,5,6,17)
kbM.init()
recStatus = 0
while True:
    keyVal = kbM.keyEvent()
    # print("input:", keyVal)
    recording   = keyVal['recordctl']
    steering    = keyVal['steering'] / 10
    throttle    = keyVal['speed'] / 10  #*maxThrottle
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

    motors.move(throttle, steering, 0.1)
    cv2.waitKey(9)