import cv2
print("package imported")

faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

#display image
img = cv2.imread("Resources/test_face.jpeg")


imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


cv2.imshow("Output", img)
cv2.waitKey(0)





"""
cap = cv2.VideoCapture("Resources/test_video.mov")

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
"""