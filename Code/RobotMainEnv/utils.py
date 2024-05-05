import cv2
import numpy as np


# Lane target detect:
# White = 255
# Black = 0

############################################################################################################
#### Function to apply black and white mask on img
############################################################################################################ 
def thesholding(img) :
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([80, 0, 0])        # [HUE Min, SAT Min, 0 ] from ColorPickSetup.py
    upperWhite = np.array([179, 160, 255])   # [HUE Max, Val Min, 255 ] from ColorPickSetup.py
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    return maskWhite

############################################################################################################
#### Function to deform perspective vision target on img
############################################################################################################
def warpImg(img, points, width, height, inv=False) :
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]]) # [widthTop, heightTop] [widthTargetTop, heightTop] [widthBottom, heightBottom] [widthTargetBottom, heightTargetBottom]
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2,pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(width,height))
    return imgWarp

def nothing(a):
    pass

############################################################################################################
#### Function to initialize setting bars before warpping function 
############################################################################################################
def initializeTrackbars(InitialTrackBarValues, wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", InitialTrackBarValues[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", InitialTrackBarValues[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", InitialTrackBarValues[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", InitialTrackBarValues[3], hT, nothing)

############################################################################################################
#### Function to get values from bar window after initialize bars
############################################################################################################
def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points

############################################################################################################
#### Function to draw red points over warp adjust window
############################################################################################################
def drawPoints(img, points):
    for x in range( 0,4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img

############################################################################################################
#### Function to draw red points over warp adjust window
############################################################################################################
def getHistogram(img, minPer=0.1, display=False, region=1):
 
    if region ==1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    if display:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return basePoint,imgHist
 
    return basePoint

############################################################################################################
#### Function to draw red points over warp adjust window
############################################################################################################
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver