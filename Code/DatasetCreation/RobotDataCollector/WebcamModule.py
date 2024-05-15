# This module gets an image through the webcam with opencv package
# -Display can be turned On/Off
# -Image size can be defined
#!/usr/bin/python3
from picamera2 import Picamera2, Preview
import cv2

class webCamera():
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.start_preview(Preview.QTGL)
        self.preview_config = self.picam2.create_preview_configuration()
        self.picam2.configure(self.preview_config)
        self.picam2.start()

    def getImg(self, display):
        frame  = self.picam2.capture_array("main")
        img = cv2.resize(frame, (640,320))       # 2:1 frame
        if display:
            cv2.imshow('cvIMG',img)
        return img

    def stopImg(self):
        self.picam2.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        imgPi = webCamera()






# from picamera.array import PiRGBArray

# 6.1.1. Capturing arrays

# initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))

# # allow the camera to warmup
# time.sleep(0.1)

# # capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array

#     # show the frame
#     cv2.imshow("Frame", image)
#     key = cv2.waitKey(1) & 0xFF

#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)

#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break

# picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)

# encoder = H264Encoder(10000000)

# picam2.start_recording(encoder, '/home/quique/Robochallenge_Charrito/Code/RobotMainEnv/test.h264') # , pts='timestamp.txt')
# time.sleep(10)




# face_detector = cv2.CascadeClassifier("/home/quique/Robochallenge_Charrito/Code/RobotMainEnv/haarcascade_frontalface_default.xml")
# cv2.startWindowThread()

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
# picam2.start()

# while True:
#     im = picam2.capture_array()

#     grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(grey, 1.1, 5)

#     for (x, y, w, h) in faces:
#         cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

#     cv2.imshow("Camera", im)
#    cv2.waitKey(1)

# cv2.startWindowThread()
# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
# picam2.start()

# cap = cv2.VideoCapture(0)




# picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)

# encoder = H264Encoder(10000000)

# picam2.start_recording(encoder, 'test.h264')
# time.sleep(10)
# picam2.stop_recording()