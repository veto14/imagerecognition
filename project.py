import cv2
import numpy as np
import argparse
import imutils
import pytesseract

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="caminho da imagem")
args = vars(ap.parse_args())

def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def opening(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def canny(img):
    return cv2.Canny(img, 200, 125)
    

img = cv2.imread('images/noise.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#custom_config = r'--oem 3 --psm 6'
custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKMNOPRSTUVWYXZ0123456789'

results = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
# display the orientation information
print("[INFO] detected orientation: {}".format(
	results["orientation"]))
print("[INFO] rotate by {} degrees to correct".format(
	results["rotate"]))
print("[INFO] detected script: {}".format(results["script"]))

# rotate the image to correct the orientation
if(results["rotate"] != 180):
    img = imutils.rotate_bound(img, angle=results["rotate"])


dst = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 6, 12) 
h, w, c = dst.shape
gray = get_grayscale(dst)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
boxes = pytesseract.image_to_boxes(dst)#, config=custom_config) 
text = pytesseract.image_to_string(dst)#, config=custom_config)
for b in boxes.splitlines():
    b = b.split(' ')
    dst = cv2.rectangle(dst, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
cv2.imshow("Image", dst)
cv2.waitKey(0)
print(text)