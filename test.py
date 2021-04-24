import time 
from imagesearch import *
import pyautogui
import cv2 as cv
#import numpy as np
import random
from auto import *
#from matplotlib import pyplot as plt

import argparse


try:

	auto_battle_active = 1
	print("Testing Auto Battler Refresher")

	while(auto_battle_active == 1):
		#check for replay button.
		change = imagesearch('./images/auto battle/replay.png')
		
		if(change[0] != -1):
			autoBattle()

	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


