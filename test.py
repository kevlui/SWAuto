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

def test():
	search('./images/battle_icon.png')
	time.sleep(2)
	search('./images/cairos_dungeon.png')
	time.sleep(2)
	search('./images/giant_tab.png')

	search('./images/gb10_icon.png')
	time.sleep(3)
	search('./images/start_battle_screen.png')
	time.sleep(2)

try:
	restart()

	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


