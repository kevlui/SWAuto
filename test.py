import time 
from imagesearch import *
import pyautogui
import cv2 as cv
import numpy as np
from auto import *
from matplotlib import pyplot as plt

import argparse

def printScreen():
	counter = 0
	pyautogui.screenshot('select_gb10.png')
	#img_rgb = cv.imread('foo.png')
	img_rgb = cv.imread("select_gb10.png")
	img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
	template = cv.imread("./images/b10.png",0)
	w, h = template.shape[::-1]
	res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
	threshold = 0.5
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		cv.rectangle(img_rgb, pt, (pt[0] + w + w, pt[1] + h), (0,0,255), 2)
		counter = counter + 1
	print(str(counter))
	cv.imwrite('result.png',img_rgb)


def test():
	rune_pos = imagesearch("./images/sixstar_2.png",0.8)
	print(rune_pos)
					
try:
	#restart()
	test()
	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


