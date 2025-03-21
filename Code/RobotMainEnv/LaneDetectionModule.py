import cv2
import numpy as np
import utils
import os
import matplotlib.pyplot as plt

curveList = []  # Buffer of image samples evaluation
avgVal = 10     # Number of image samples evaluation

def preProcess(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    imgBlur2 = cv2.GaussianBlur(imgGray, (5, 5), 0) 
    imgCanny2 = cv2.Canny(imgBlur2, 50, 150)
    return imgCanny2

def region_of_interest(canny):
    height = canny.shape[0]
    width = canny.shape[1]
    mask = np.zeros_like(canny)
 
    triangle = np.array([[
    (10, height),
    (315, 150),
    (630, height),]], np.int32)
 
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image

def make_points(image, line):
    slope, intercept = line
    y1 = int(image.shape[0])# bottom of the image
    y2 = int(y1*3/5)         # slightly lower than the middle
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit    = []
    right_fit   = []
    # if lines is None:
    #     return None
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         fit = np.polyfit((x1,x2), (y1,y2), 1)
    #         slope = fit[0]
    #         intercept = fit[1]
    #         if slope < 0: # y is reversed in image
    #             left_fit.append((slope, intercept))
    #         else:
    #             right_fit.append((slope, intercept))
    # # add more weight to longer lines
    # left_fit_average  = np.average(left_fit, axis=0)
    # right_fit_average = np.average(right_fit, axis=0)
    # left_line  = make_points(image, left_fit_average)
    # right_line = make_points(image, right_fit_average)
    # averaged_lines = [left_line, right_line]
    # return averaged_lines
    if len(left_fit) and len(right_fit):
        ##over-simplified if statement (should give you an idea of why the error occurs)
        left_fit_average  = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line  = make_points(image, left_fit_average)
        right_line = make_points(image, right_fit_average)
        averaged_lines = [left_line, right_line]
    return averaged_lines
        

def display_lines(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image


def getLaneCurve(img, display) :
    imgCopy = img.copy()
    imgResult = img.copy()
    
    # EXAMPLE WITH FINDING LANES:
    path = os.path.abspath(os.path.join(os.getcwd(), '../Robochallenge_Charrito/Code/RobotMainEnv/test_image.jpg'))
    image1 = cv2.imread(path)
    image = cv2.resize(image1, (utils.WIDHT_SCREEN_SIZE, utils.HEIGHT_SCREEN_SIZE))
    img_lane = np.copy(image)
    imgCanny2 = preProcess(img_lane)
    cropCanny = region_of_interest(imgCanny2)


    # lines = cv2.HoughLinesP(cropCanny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
    # averaged_lines = average_slope_intercept(img_lane, lines)
    # line_image = display_lines(img_lane, averaged_lines)
    cv2.imshow('lane_detect', cropCanny)
    # plt.imshow("result", cropCanny)
    # plt.show()

    ##### STEP 1: REDUCE NOISE WITH BLUR AND SHARP GRADIENT INTENSITY
    imgBlur = cv2.GaussianBlur(img, (5, 5), 0) 
    
    ##### STEP 2: CREATE MASK BLACK/WHITE
    imgThres = utils.thesholding(imgBlur)
    imgInvert = cv2.bitwise_not(imgThres)
    imgCanny = cv2.Canny(imgInvert, 50, 150)    # (image, low_threshold, high_threshold)

    ##### STEP 3:  CREATE POINTS OVER TRACK TO LIMIT VISION FIELD (REGION OF INTEREST)
    points = utils.valTrackbars()
    imgWarpPoints = utils.drawPoints(imgCopy, points) 
    # cv2.imshow('cvWarp Points', imgWarpPoints)
    height, width, c = img.shape
    imgWarp = utils.warpImg(imgInvert, points, width, height, invert=False)
    
    ##### STEP 4:  FINDING LANE OUTLINES
    # for i,j in range points(2,4)
    # polygon = np.array([(points[0]), (points[1]), (points[2]), (points[3])])
    # polygonInt = polygon[:,].astype(int)
    # polygon = np.array([(75, 83), (565, 830), (0, 360), (640, 360)])
    # print(polygon)
    # imgMask = np.zeros_like(img)
    # for poly in points:
    #    cv2.fillPoly(imgMask, polygon[poly], color=(255, 0, 0))
    # cv2.fillPoly(imgMask, polygon, 255)

    ##### STEP 5: GET THE AVERAGE POINT IN LANE
    middlePoint = utils.getHistogram(imgWarp, display=False, minPer=0.1, region=1)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9, region=4)
    curveRaw = curveAveragePoint - middlePoint
    #print('cuve val:', curveRaw)

    # ##### STEP 6: SMOOTHING CURVE EVALUATE TEN SAMPLES
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
         curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    ##### STEP 7: DRAW HISTOGRAM RESULT AND SHOWS ALL WINDOWS IN ONE
    if display != 0:
       imgInvWarp = utils.warpImg(imgWarp, points, width, height, invert=True) # Invert warp
       imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:height//3,0:width] = 0, 0, 0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
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
       print('imgShow')
       # imgStacked = utils.stackImages(0.7,([imgWarpPoints, imgCanny, imgCanny2],   #imgWarp      # Align imgs processing in a single window
       #                                  [imgHist, imgLaneColor, imgResult]))
       #cv2.imshow('cvImageStack',imgStacked)
    
    elif display == 1:
        cv2.imshow('cvOrig', imgCopy)
        cv2.imshow('cvWarp', imgWarp)
        cv2.imshow('cvCanny', imgCanny)
        cv2.imshow('cvResult',imgResult)
        # cv2.imshow('cvThres', imgThres)
        # cv2.imshow('cvInvert', imgInvert)
        # cv2.imshow('cvBlur', imgBlur)
        # cv2.imshow('cvMask', imgMask)
    
    # NORMALIZE CURVE RESULT
    curve = curve/100
    if curve > 1: curve = 1
    if curve <-1: curve =-1

    # return None
    return curve

if __name__ == '__main__' :
    print('OpenCV version: ', cv2.__version__)
    # pathfile = pathlib.Path(__file__).parent.resolve()
    # print(pathfile)
    # RPi 5 Env:
    # cap = cv2.imread('/home/quique/Robochallenge_Charrito/Code/RobotMainEnv/devOps_diagram.jpeg', cv2.IMREAD_GRAYSCALE)
    # Windows Env:
    # img2 = cv2.imread('C:/Users/10753308/Robochallenge_Charrito/Code/RobotMainEnv/devOps_diagram.jpeg')

    pathVideo = os.path.abspath(os.path.join(os.getcwd(), '../Robochallenge_Charrito/Code/RobotMainEnv/Vid1.mp4'))
    # pathVideo = os.path.abspath(os.path.join(os.getcwd(), '../Robochallenge_Charrito/Code/RobotMainEnv/test_image.jpg'))
    cap = cv2.VideoCapture(pathVideo) #Windows requires complete filepath
    initialTrackBarValues = [0, 360, 165, 44]   # 0, 360, 110, 90 [wT, hT, wB, hB]
    utils.initializeTrackbars(initialTrackBarValues)
    frameCounter = 0
    curveList=[]
    while True:
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
             frameCounter=0
        success, img = cap.read()
        img = cv2.resize(img, (utils.WIDHT_SCREEN_SIZE, utils.HEIGHT_SCREEN_SIZE))
        # cv2.imshow('VidOriginal', img)
        curve = getLaneCurve(img, display=0)       # display=0 none, 1=separate windows, 2=all in one window 
        print('curve val:', curve)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

