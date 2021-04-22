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
	sell_pos = imagesearch("./images/sell.png")
	if(sell_pos[0] != -1):
		print("found.")
	else:
		print("not found.")

	


except KeyboardInterrupt:	
	print("Keyboard Interrupt")


