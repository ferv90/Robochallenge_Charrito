import cv2
import numpy as np
import utils

curveList = []  # Buffer of image samples evaluation
avgVal = 10     # Number of image samples evaluation

def getLaneCurve(img, display) :
    imgCopy = img.copy()
    imgResult = img.Copy()
    
    ##### STEP 1: CREATE MASK BLACK/WHITE (GRAYSCALE)
    imgThres = utils.thesholding(img)
    
    ##### STEP 2: REDUCE NOISE WITH BLUR AND SHARP GRADIENT INTENSITY
    # imgBlur = cv2.GaussianBlur(imgThres, (5, 5), 0) 
    # imgcanny = cv2.Canny(imgBlur, 50, 150)    # (img, low_threshold, high_threshold)

    ##### STEP 3:  CREATE POINTS OVER TRACK TO LIMIT VISION FIELD (REGION OF INTEREST)
    height, width, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(img, points, width, height, inv=False)
    imgWarpPoints = utils.drawPoints(imgCopy, points)

    ##### STEP 4:  FINDING LANE OUTLINES
    # imgMask = np.zeros(imgWarp)
    # cv2.fillPoly(imgMask, imgWarpPoints, 255)

    ##### STEP 5: GET THE AVERAGE POINT IN LANE
    middlePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    ##### STEP 6: SMOOTHING CURVE EVALUATE TEN SAMPLES
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    ##### STEP 7: DRAW HISTOGRAM RESULT AND SHOWS ALL WINDOWS IN ONE
    if display != 0:
       imgInvWarp = utils.warpImg(imgWarp, points, width, height,inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:height//3,0:width] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult, str(curve), (width//2-80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
       cv2.line(imgResult, (width//2, midY), (width//2+(curve*3), midY), (255, 0, 255), 5)
       cv2.line(imgResult, ((width // 2 + (curve * 3)), midY-25), (width // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = width // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       # cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    
    if display == 2:
       imgStacked = utils.stackImages(0.7,([img, imgWarpPoints, imgWarp],         # Align imgs processing in a single window
                                         [imgHist, imgLaneColor, imgResult]))
       cv2.imshow('cvImageStack',imgStacked)
    
    elif display == 1:
       cv2.imshow('cvResult',imgResult)

    # NORMALIZE CURVE RESULT
    curve = curve/100
    if curve > 1: curve = 1
    if curve <-1: curve =-1

    cv2.imshow('cvThres', imgThres)
    cv2.imshow('cvWarp', imgWarp)
    # cv2.imshow('cvBlur', imgBlur) or Canny
    # cv2.imshow('cvBlur', imgMask)
    cv2.imshow('cvWarp Points', imgWarpPoints)
    cv2.imshow('cvHistogram', imgHist)
    # return None
    return curve


if __name__ == '__main__' :
    cap = cv2.VideoCapture('vid1.mp4')
    initialTrackBarValues = [110, 208, 0, 280]
    utils.initializeTrackbars(initialTrackBarValues)
    frameCounter = 0
    curveList=[]
    while True:
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        success, img = cap.read()
        img = cv2.resize(img, (480,240))
        curve = getLaneCurve(img, display=1)       # display=0 none, 1=separate windows, 2=all in one window 
        print(curve)
        # cv2.imshow('VidOriginal', img)
        cv2.waitKey(0)


