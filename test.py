import time 
from imagesearch import *
import pyautogui
import cv2 as cv
import numpy as np
import random
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
	if(search("./images/replay.png") == -1):
				search("./images/halloween_event.png")
				search("./images/ok.png")


def test_click():
	time.sleep(3)
	pyautogui.moveTo(500,400, 2, pyautogui.easeInOutQuad)
	time.sleep(.5)
	pyautogui.moveTo(1300,400, 2, pyautogui.easeInOutQuad)
	time.sleep(.5)


def test_click_loop():
	 x = random.randint(70,120)

	 while x > 0:
	 	test_click()
	 	x = random.randint(70,120)
	 	print(x)
	 	time.sleep(x)
			
try:
	restart(4)
	#autoplay_pos = search("./images/autoplay_button_nb10.png")
	#test_click_loop()

	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


