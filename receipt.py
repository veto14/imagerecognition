import cv2
import numpy as np
import pytesseract

def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def opening(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def canny(img):
    return cv2.Canny(img, 200, 125)

img = cv2.imread('invoice.jpg')
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
h, w, c = img.shape
dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15) 
gray = get_grayscale(dst)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
boxes = pytesseract.image_to_boxes(dst) 
text = pytesseract.image_to_string(dst)
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(dst, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
cv2.imshow("Image", img)
cv2.waitKey(0)
print(text)