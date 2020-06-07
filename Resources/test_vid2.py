import cv2
import pafy
import time
import datetime




url = "https://www.youtube.com/watch?v=8YuBxP4CKZc"
vpafy = pafy.new(url)
play = vpafy.getbest(preftype="mp4")




# Load the cascade
face_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_mcs_mouth.xml')


# To capture video from webcam.
#cap = cv2.VideoCapture('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/test_face.mov')
cap = cv2.VideoCapture("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/satsang_test.mov")#play.url
video_path = "/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/satsang_test.mov"

cap.set(cv2.CAP_PROP_POS_FRAMES, 25000)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')


frame_rate = 100
prev = 0

count = 0

ds_factor = 0.5

now = time.perf_counter()

while True:
    print(time.perf_counter())
    # Read the frame
    time_elapsed = time.time() - prev
    _, img = cap.read()

    if time_elapsed > 1. / frame_rate:
        prev = time.time()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)


        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.16, 6)#1.7,11

        for (x, y, w, h) in mouth_rects:
            count += 1
            if (count == 1):
                currentTime = time.time()
                finalTime = currentTime + 10
            elif time.time() >= finalTime:
                if((count > 30) and (count < 85)):
                    print("Talking")
                    cv2.putText(img, "Talking", (x-50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
                count = 0
            elif time.time() < finalTime:
                print(count)
            #print("mouth")
            y = int(y - 0.15 * h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            #cv2.putText(img, "Movement", (x-50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            break

        # Display

        cv2.imshow('img', img)



    # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break









# Release the VideoCapture object
cap.release()