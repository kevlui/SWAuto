import time 
from imagesearch import *
import pyautogui
import cv2 as cv
import numpy as np
from auto import *
from matplotlib import pyplot as plt

def printScreen():
	counter = 0
	pyautogui.screenshot('time_test.png')
	#img_rgb = cv.imread('foo.png')
	img_rgb = cv.imread("time_test.png")
	img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
	template = cv.imread("./images/time_icon.png",0)
	w, h = template.shape[::-1]
	res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
	threshold = 0.5
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
	    cv.rectangle(img_rgb, pt, (pt[0] + w + w, pt[1] + h), (0,0,255), 2)
	cv.imwrite('result.png',img_rgb)

def search_loop(image_directory):
	search_bool = 0
	while(search_bool != 1):
		search_pos = imagesearch(image_directory)
		if(search_pos[0] != -1):
			search(image_directory)
			search_bool = 1

try:
	#printScreen()
	#getRuneStats()
	if(isRuneType("swift")):
		if(hasSPD()):
			print ("Swift Rune with SPD Sub")
	elif(isRuneType("energy")):
		print("Energy Rune.")
	elif(isRuneType("fatal")):
		print("Fatal Rune.")
	elif(isRuneType("despair")):
		print("despair Rune.")
	elif(isRuneType("blade")):
		print("blade Rune.")
	else:
		print ("Rune sold.")
except KeyboardInterrupt:	
	print("Keyboard Interrupt")


