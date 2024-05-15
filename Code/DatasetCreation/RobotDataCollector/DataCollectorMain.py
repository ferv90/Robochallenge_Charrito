import WebcamModule as wM
import DataCollectionModule as dcM
import KeyboardGameModule as kbM
import MotorModule as robot
import cv2
from time import sleep

maxThrottle = 0.258
motors = robot.Motors(12,19,16,13,6,5,17)


kbM.init()
recStatus = 0
while True:
    keyVal = kbM.keyEvent()
    # print("input:", keyVal)
    recording   = keyVal['recordctl']
    steering    = keyVal['steering'] / 10
    throttle    = keyVal['speed'] / 10  #*maxThrottle

    # START/STOP RECODING WITH SPACE BAR OVER KB_PYGAME WINDOW
    if recording == 1 and recStatus == 0:
        camera = wM.webCamera()
        print('Recording Started ...')
        sleep(2)
        recStatus +=1

    # SAVING IMAGES AND STEERING ANGLE IN REAL TIME
    if recStatus == 1:
        img = camera.getImg(display=True)    # Get image from webcam
        print("Save data steering")
        dcM.saveData(img,steering)

    # STOP RECORDING WITH 'SPACE_BAR' OVER KB_PYGAME WINDOW
    if recording == 2 and recStatus == 1:
        print("Stop data record and save log file...")
        dcM.saveLog()
        camera.stopImg()
        sleep(2)
        recStatus = 0

    motors.move(throttle, steering, 0.1)
    cv2.waitKey(9)