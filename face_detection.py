import cv2
import pafy
import time
import pytesseract

from moviepy.editor import VideoFileClip
from PIL import Image


url = "https://www.youtube.com/watch?v=8YuBxP4CKZc"
vpafy = pafy.new(url)
play = vpafy.getbest(preftype="avi")




# Load the cascade
face_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_mcs_mouth.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer.read("trainner.yml")


# To capture video from webcam.
#cap = cv2.VideoCapture('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/test_face.mov')
video_path = "/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/satsang_test.mov"
video_path2 = "/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/clip_1.avi"

cap = cv2.VideoCapture(video_path)#play.url





cap.set(cv2.CAP_PROP_POS_FRAMES, 50000)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

num=0
frame_rate = 100
prev = 0

count = 0
startTime = 0
endTime = 0
ds_factor = 0.5

startTimeSet = []
endTimeSet = []

now = time.perf_counter()
timeStamps = []
start_time = time.time()
#ffmpeg_extract_subclip(video_path, int(0), int(100), targetname=str("ammvidNum" + str(num)) + ".mp4")
#clip = VideoFileClip(video_path).subclip(0, 100)
#clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" + str(num) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

while True:

    time_elapsed = time.time() - prev
    _,img = cap.read()
    _,img2 = cap.read()


    if time_elapsed > 1. / frame_rate:
        prev = time.time()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #DETECT FACES

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        #dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        #ontours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,

                                               #cv2.CHAIN_APPROX_NONE)
        #im2 = img.copy()


        # Drawing a rectangle on copied image

        rect = cv2.rectangle(img, (1, 357), (169, 330), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = img[357:330, 1:1 + 168]


        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Face,", (x - 30, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.16, 6)

        for(x, y, w, h) in mouth_rects:
            count+=1
            if (count== 1):
                currentTime = time.time()
                finalTime = currentTime + 10
            elif time.time() >= finalTime:
                img2[img2 >= 200] = 76
                img2[img2 != 76] = 255
                img2[img2 == 76] = 0
                img3 = Image.fromarray(img2).convert('L')
                img3 = img3.crop((0, 330, 168, 357))
                print(img3)
                Image._show(img3)
                result = pytesseract.image_to_string(img3, lang='eng')
                print(result)
                #del(img3)
                if((count > 25) and (count < 85)):
                    print("Talking")
                    timeStamps.append(time.perf_counter())
                    if(len(timeStamps)==1):
                        startTime = (time.time() - start_time) - 30
                        startTimeSet.append(startTime)
                        print("started")
                    cv2.putText(img, "Talking", (x-50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
                    if(len(timeStamps) > 1):
                        if(timeStamps[-1] -  timeStamps[-2] < 60):
                            print("Likely Talking")
                        else:
                            if(startTime - endTime < 40):
                                startTimeSet.remove(startTimeSet[-1])
                                if(len(endTimeSet)>0):
                                    endTimeSet.remove(endTimeSet[-1])
                            else:
                                endTime = (time.time() - start_time) + 20
                                endTimeSet.append(endTime)
                                num+=1
                            print("ended")
                            startTime = 0
                            endTime = 0
                            timeStamps.clear()
                    print(*timeStamps)
                count = 0
            elif time.time() < finalTime:
                print(count)
            elif time.time() > finalTime:
                print(count)

            y = int(y - 0.15 * h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            break

        # Display
        #print(time.time() - start_time)
        cv2.imshow('img', img)



    # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

num = 0
for i in startTimeSet:

    clip = VideoFileClip(video_path).subclip(startTimeSet[num], endTimeSet[num])
    clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                  str(num) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                  remove_temp=True, audio_codec='aac')
    num+=1






# Release the VideoCapture object
cap.release()