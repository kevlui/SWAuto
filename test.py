import time 
import pyautogui
import cv2 as cv
import random
from auto import *
from imagesearch import *
import logging 


import argparse





try:
	logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w') 
	logger=logging.getLogger() 
	logger.setLevel(logging.DEBUG) 

	print("Auto Battler Refresher Start")
	logging.debug("Testing Debug method.")
	autoBattle(0,3)
	#search('./images/auto battle/repeat_battle.png')
	


	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


