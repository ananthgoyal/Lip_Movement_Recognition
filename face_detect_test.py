import cv2
print("package imported")


#faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

#imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.imread("Resources/test_face.jpeg")
cv2.imshow("Output", img)
cv2.waitKey(1000)

"""

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


cv2.imshow("Output", img)
cv2.waitKey(0)
"""