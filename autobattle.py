import time 
import pyautogui
import cv2 as cv
import random
from auto import *
from imagesearch import *
import logging 
import argparse

def start(n):
	logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w') 
	logger=logging.getLogger() 
	logger.setLevel(logging.DEBUG) 
	
	print("Auto Battler Refresher Start")
	print("Number of Refills: " + str(n))
	logging.debug("Testing Debug method.")
	autoBattle(0,n)


try:
	refills = 10
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num', dest = "refills", default = 0 , type = int)
	args = parser.parse_args()
	start(refills)

	#toa()

except KeyboardInterrupt:	
	print("Keyboard Interrupt")

