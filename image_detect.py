import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/haarcascade_mcs_mouth.xml')

# Read the input image
img = cv2.imread('/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/Images/reg_imgs/aaron.jpg')

# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
mouth = mouth_cascade.detectMultiScale(gray, 1.16, 6)

# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

for(x, y, w, h) in mouth:
    y = int(y - 0.15 * h)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

# Display the output
cv2.imshow('img', img)
cv2.waitKey()