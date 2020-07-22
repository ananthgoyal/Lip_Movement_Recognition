import pytesseract
# adds image processing capabilities
from PIL import Image

# converts the text to speech


img = Image.open('testpic.png')
print(img)
result = pytesseract.image_to_string(img)
print(result)