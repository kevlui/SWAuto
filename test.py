import time 
import pyautogui
import cv2 as cv
import random
from auto import *
from imagesearch import *
from quizsolver import *
import logging 
import argparse




def toah():
	conditional = -1
	loop = 1
	fails = 0

	print("Testing Toa.")

	while(loop == 1):
		while(conditional == -1):
			pos = imagesearch("./images/victory-paint.png")
			pos2 = imagesearch("./images/no.png")
					
			if(pos[0] != -1):			#If Victory img is found
				conditional = 1
				print(conditional)
			elif(pos2[0] != -1):		#If Fail is found.
				conditional = 2

		#If run is successful:
		if(conditional == 1):
			toa()

		elif(conditional == 2):
			logging.info("Script has ended.")
			sys.ext()




try:
	#logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w') 
	#logger=logging.getLogger() 
	#logger.setLevel(logging.DEBUG) 
	
	#print("Auto Battler Refresher Start")
	#logging.debug("Testing Debug method.")
	#autoBattle(0,1)
	quizSolver()
	
		


	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


