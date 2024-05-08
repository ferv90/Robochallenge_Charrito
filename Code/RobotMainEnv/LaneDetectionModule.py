import cv2
import numpy as np
import utils
import pathlib

curveList = []  # Buffer of image samples evaluation
avgVal = 10     # Number of image samples evaluation

def getLaneCurve(img, display) :
    imgCopy = img.copy()
    imgResult = img.copy()
    
    ##### STEP 1: REDUCE NOISE WITH BLUR AND SHARP GRADIENT INTENSITY
    imgBlur = cv2.GaussianBlur(img, (5, 5), 0) 
    
    ##### STEP 2: CREATE MASK BLACK/WHITE
    imgThres = utils.thesholding(imgBlur)
    imgCanny = cv2.Canny(imgThres, 50, 150)    # (image, low_threshold, high_threshold)

    ##### STEP 3:  CREATE POINTS OVER TRACK TO LIMIT VISION FIELD (REGION OF INTEREST)
    points = utils.valTrackbars()
    imgWarpPoints = utils.drawPoints(imgCopy, points)
    # cv2.imshow('cvWarp Points', imgWarpPoints)
    height, width, c = img.shape
    imgWarp = utils.warpImg(imgCanny, points, width, height, invert=False)
    
    ##### STEP 4:  FINDING LANE OUTLINES
    # for i,j in range points(2,4)
    # polygon = np.array([(points[0]), (points[1]), (points[2]), (points[3])])
    # polygonInt = polygon[:,].astype(int)
    polygon = np.array([(75, 83), (565, 830), (0, 360), (640, 360)])
    print(polygon)
    imgMask = np.zeros_like(img)
    # for poly in points:
    #    cv2.fillPoly(imgMask, polygon[poly], color=(255, 0, 0))
    # cv2.fillPoly(imgMask, polygon, 255)

    ##### STEP 5: GET THE AVERAGE POINT IN LANE
    middlePoint = utils.getHistogram(imgWarp, display=False, minPer=0.5, region=1)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9, region=4)
    curveRaw = curveAveragePoint - middlePoint
    print(curveRaw)

    # ##### STEP 6: SMOOTHING CURVE EVALUATE TEN SAMPLES
    # curveList.append(curveRaw)
    # if len(curveList)>avgVal:
    #     curveList.pop(0)
    # curve = int(sum(curveList)/len(curveList))

    ##### STEP 7: DRAW HISTOGRAM RESULT AND SHOWS ALL WINDOWS IN ONE
    # if display != 0:
    #    imgInvWarp = utils.warpImg(imgWarp, points, width, height,inv = True)
    #    imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
    #    imgInvWarp[0:height//3,0:width] = 0,0,0
    #    imgLaneColor = np.zeros_like(img)
    #    imgLaneColor[:] = 0, 255, 0
    #    imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
    #    imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
    #    midY = 450
    #    cv2.putText(imgResult, str(curve), (width//2-80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
    #    cv2.line(imgResult, (width//2, midY), (width//2+(curve*3), midY), (255, 0, 255), 5)
    #    cv2.line(imgResult, ((width // 2 + (curve * 3)), midY-25), (width // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
    #    for x in range(-30, 30):
    #        w = width // 20
    #        cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
    #                 (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
    #    # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    #    # cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    
    # if display == 2:
    #    imgStacked = utils.stackImages(0.7,([img, imgWarpPoints, imgWarp],         # Align imgs processing in a single window
    #                                      [imgHist, imgLaneColor, imgResult]))
    #    cv2.imshow('cvImageStack',imgStacked)
    
    # elif display == 1:
    #    cv2.imshow('cvResult',imgResult)

    # NORMALIZE CURVE RESULT
    # curve = curve/100
    # if curve > 1: curve = 1
    # if curve <-1: curve =-1

    #cv2.imshow('cvThres', imgThres)
    
    #cv2.imshow('cvBlur', imgBlur)
    cv2.imshow('cvCanny', imgCanny)
    
    # cv2.imshow('cvMask', imgMask)
    cv2.imshow('cvWarp', imgWarp)
    
    cv2.imshow('cvHistogram', imgHist)
    return None
    # return curve


if __name__ == '__main__' :
    print('OpenCV version: ', cv2.__version__)
    # pathfile = pathlib.Path(__file__).parent.resolve()
    # print(pathfile)
    # img2 = cv2.imread('C:/Users/10753308/Robochallenge_Charrito/Code/RobotMainEnv/devOps_diagram.jpeg')
    cap = cv2.VideoCapture('C:/Users/10753308/Robochallenge_Charrito/Code/RobotMainEnv/Vid1.mp4') #Windows requires complete filepath
    initialTrackBarValues = [0, 360, 75, 83]   # 0, 360, 110, 90 [wT, hT, wB, hB]
    utils.initializeTrackbars(initialTrackBarValues)
    frameCounter = 0
    # curveList=[]
    while True:
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
             cap.set(cv2.CAP_PROP_POS_FRAMES,0)
             frameCounter=0
        success, img = cap.read()
        img = cv2.resize(img, (utils.WIDHT_SCREEN_SIZE, utils.HEIGHT_SCREEN_SIZE))
        cv2.imshow('VidOriginal', img)
        
        curve = getLaneCurve(img, display=1)       # display=0 none, 1=separate windows, 2=all in one window 
        # print(curve)
        # cv2.imshow('VidOriginal', img)
        cv2.waitKey(1)

