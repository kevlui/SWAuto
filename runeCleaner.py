import time 
import pyautogui
import sys
from imagesearch import *
from auto import *
from datetime import datetime
import os
import random
import logging 

import cv2
import numpy as np
import pandas as pd
import math 

import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'.\hello tess\tesseract.exe'

'''
cropRune() - crops the rune info while in the powerup screen
'''
def cropRune():
	powerup = quizSearch('./images/rune_cleaner/powerup_result.png')
	img = cv2.imread('./images/rune_cleaner/dummy_rune.png')
	height, width, channels = img.shape

	valid = False

	while(valid == False):
		cross = quizSearch('./images/rune_cleaner/close.png')
		ok = quizSearch('./images/rune_cleaner/ok.png')
		six = quizSearch('./images/rune_cleaner/6-stars.png')

		botx = cross[0]
		boty = ok[1] - 100

		#Search for the 2nd 6-star
		target = imagesearcharea("./images/rune_cleaner/6-stars.png",powerup[0],powerup[1],botx,boty, 0.7)
		print(target)

		topx = powerup[0] + target[0] - 10
		topy = powerup[1] + target[1] + height

		if((botx > topx) and (boty > topy)):
			print("Values valid.")
			screenshot = pyautogui.screenshot()
			screenshot = np.array(screenshot)
			screenshot = cv2.rectangle(screenshot, (topx,topy), (botx,boty), (0,255,0) , 3)
			cv2.imwrite("sellTestScreenShot.png", screenshot)
			valid = True
		else:
			print("Values invalid - Recalculating.")

	print([topx, topy, botx, boty])
	screenshot = region_grabber([topx, topy, botx, boty])

	return screenshot

'''
cropRuneScreen() - crops the rune info while in the rune inventory screen.
'''
def cropRuneScreen():
	img = cv2.imread('./images/rune_cleaner/dummy_rune_screen.png')
	height, width, channels = img.shape

	valid = False

	while(valid == False):
		six = quizSearch('./images/rune_cleaner/6-stars-screen.png')
		sell = quizSearch('./images/rune_cleaner/sell.png')

		topx = six[0] - 10
		topy = six[1] + height


		if((sell[0] > topx) and (sell[1] > topy)):
			print("Values valid.")

			screenshot = pyautogui.screenshot()
			screenshot = np.array(screenshot)
			screenshot = cv2.rectangle(screenshot, (topx,topy), (sell[0],sell[1]), (0,255,0) , 3)
			cv2.imwrite("sellTestScreenShot.png", screenshot)

			valid = True
		else:
			print("Values invalid - Recalculating.")

	print([topx, topy, sell[0], sell[1]])
	screenshot = region_grabber([topx,topy,sell[0],sell[1]])
	return screenshot

'''
calculateRunePoints() - calculates the rune point value using the Hitchhiker method
'''

def calculateRunePoints(img):
	#Parse images
	img_text = pytesseract.image_to_string(img)
	img_text2 = img_text.replace('\n'," ")
	wordList = img_text2.split(" ")
	#Get the subs
	allSubs = ["HP","DEF", "ATK","SPD", "Rate", "Dmg", "Resistance", "Accuracy"]
	runeSubs = []

	total = 0
	weighted = 0
	parsedSubValue = 0

	for sub in allSubs:
		for index,item in enumerate(wordList):
			if(item == sub):
				runeSubs.append(sub)
				runeSubs.append(wordList[index + 1])

				#Non-flat stats:
				if "%" in wordList[index + 1]:

					parsedSubValue = wordList[index + 1].replace("%", "")
					parsedSubValue = int(parsedSubValue)

					if(item == "Resistance" or item == "Accuracy"):
						total = total + parsedSubValue
					elif (item == "Rate"):
						weighted = weighted + math.ceil(1.5 * (parsedSubValue))
					else:
						weighted = weighted + parsedSubValue
				#Flat-Stats
				else:

					parsedSubValue = wordList[index + 1].replace("+", "")
					parsedSubValue = int(parsedSubValue)

					if (item == "SPD"):
						weighted = weighted + (2 * (parsedSubValue))


	print(runeSubs)
	print("WEIGHTED: ", weighted)
	print("TOTAL: ", weighted + total)



try:
	test = 0
	wait = 0

	print("Starting Up Rune Cleaner.")

	while(test == 0):
		powerup = quizSearch('./images/rune_cleaner/powerup_result.png')
		sell = quizSearch('./images/rune_cleaner/sell.png')

		if(sell != -1):
			calculateRunePoints(cropRuneScreen())

			#Wait until the sell button is gone.
			while(wait == 0):
				sell = quizSearch('./images/rune_cleaner/sell.png')

				if(sell == -1):
					wait = 1

			wait = 0

		elif(powerup != -1):
			calculateRunePoints(cropRune())

			#Wait until the powerup is gone:
			while(wait == 0):
				powerup = quizSearch('./images/rune_cleaner/powerup_result.png')


				if(powerup == -1):
					wait = 1

			wait = 0




except KeyboardInterrupt:	
	print("Keyboard Interrupt")