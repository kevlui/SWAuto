import time 
from imagesearch import *
import pyautogui
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def search(image_directory):
	time.sleep(1)
	button = imagesearch(image_directory)
	if button[0] != -1:
		click_image(image_directory, button, "left", 0.2, offset=5)
	else:
		print(image_directory + "is not found")

def printScreen():
	counter = 0
	#pyautogui.screenshot('quiz_test.png')
	#img_rgb = cv.imread('foo.png')
	img_rgb = cv.imread("quiz_test.png")
	img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
	template = cv.imread("./images/quiz.png",0)
	w, h = template.shape[::-1]
	res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
	threshold = 0.5
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
	    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	cv.imwrite('result.png',img_rgb)



def findTest():
	quiz_pos = imagesearch('./images/quiz.png')
	if(quiz_pos[0] != -1):
		print("Test found.")
		#pyautogui.screenshot("quiz.png")
		search('./images/bs_close.png')
		#search('./images/bs_yes.png')
		#sys.exit()
	else:
		print("Test not found.")


try:
	findTest()

except KeyboardInterrupt:	
	print("Keyboard Interrupt")


