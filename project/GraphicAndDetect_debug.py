import cv2
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import imutils
import cv2

# 處理CV2 putText中文
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):  #判斷是否OpenCV圖片類型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/mingliu.ttf", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)

class Camera(object):
    def __init__(self, resolution=(320, 240), framerate=32, **kwargs, ):
        # face detector
        cascPath = "/home/pi/Desktop/Labs/1092/IESD/Lab7/ref/example_code/model/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        
        # initialize the camera
        self.camera = PiCamera()

        # set camera parameters
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        print(self.camera.zoom)

        # framerate counter
        self.t0 = time.time()
        self.t1 = time.time()

        # set optional camera parameters (refer to PiCamera docs)
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        # initialize the stream
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.msg = ""
        self.detect = True
        self.face_num = 0
        self.frame = None
        self.stopped = False
        self.start()
        time.sleep(2)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def face_detector_switch(self, state):
        self.detect = state

    def update_msg(self, msg):
        self.msg = msg

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            #MY CODE BEGIN
            
            image = imutils.resize(f.array, height=600)

            self.t1 = time.time()
            fps = round(1 / (self.t1-self.t0),1)
            self.t0 = time.time()

            if self.detect:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(200, 200)
                )
                self.face_num = len(faces)

                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                cv2.rectangle(image, (int(image.shape[1]/2-100), 200), (int(image.shape[1]/2+100), 400), (0, 0, 255), 2)

            text_area = np.ones([600,400,3],dtype="uint8")*255

            text_area = cv2ImgAddText(text_area, self.msg, 20, 20, 
                        textColor=(0,0,0),textSize=12)

            # lines = self.msg.splitlines()
            # y0, dy = 20, 24
            # for line in lines:
            #     cv2.putText(text_area, line, (20, y0), 
            #             cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0,0,0))
            #     y0 += dy

            # put fps
            cv2.rectangle(image, (0, 0), (50, 20), (0, 0, 255), -1)
            cv2.putText(image, str(fps), (5, 15), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,0))

            self.frame = cv2.hconcat([image, text_area])
            
            #MY CODE END
            self.rawCapture.truncate(0)


            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def get_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tostring()

    def __del__(self):
        self.stop()
        time.sleep(0.5)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
