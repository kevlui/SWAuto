import time 
import pyautogui
import sys
from imagesearch import *
from datetime import datetime
import os
import random



def search(image_directory):
	delay = random.randint(3,4)
	button = imagesearch(image_directory)
	if button[0] != -1:
		#print("Delay is: " + str(delay) + " seconds")
		click_image(image_directory, button, "left", 0.2, offset=5)
		time.sleep(delay)
	else:
		print(image_directory + " is not found")
		return -1

def search_loop(image_directory):
	search_bool = 0
	while(search_bool != 1):
		search_pos = imagesearch(image_directory)
		if(search_pos[0] != -1):
			search(image_directory)
			search_bool = 1

def closeAds():
	ad = 0
	while(ad < 5):
		start_ad_pos = imagesearch('./images/start_ad_close.png')
		if(start_ad_pos[0] != -1):
			search('./images/start_ad_close.png')
			ad = ad + 1
		else:
			ad = 10

def clickB10():
	button = imagesearch('./images/b10.png')
	end = imagesearch('./images/shake_icon.png')
	result = imagesearcharea('./images/start_battle_screen2.png', button[0] , button [1] , end[0], end[1])
	final = (button[0] + result[0], button[1] + result[1])
	click_image('./images/start_battle_screen2.png',final, "left", 0.2, offset=5)
	time.sleep(2)


def restart(mode):
	#Restart the application
	search('./images/sw_tab.png')
	time.sleep(0.5)
	search('./images/sw_close.png')
	search('./images/sw_icon.png')

	clickLocation = imagesearch('./images/sw_icon.png')

	time.sleep(10)
	closeAds()

	#click_image('./images/sw_icon.png', clickLocation , "left", 0.2, offset=5)

	#Check for "Touch to start"
	restart = -1
	while(restart == -1):
		start_pos = imagesearch('./images/title_screen.png')
		if(start_pos[0] != -1):
			restart = 0

	time.sleep(30)
	closeAds()

	search('./images/title_screen.png')
	time.sleep(2)
	search('./images/sw_intro_skip.png')

	time.sleep(2)
	search('./images/ad_close_2.png')
	time.sleep(.5)
	search('./images/ad_close_3.png')
	time.sleep(5)

	search('./images/battle_icon.png')
	time.sleep(5)

	#dimensionalRiftBypass()
	search('./images/cairos_dungeon.png')
	time.sleep(2)

	if(mode == 1):
		search('./images/giant_tab.png')
	elif(mode == 4):
		search("./images/necropolis_tab.png")
	elif(mode == 5):
		search("./images/dragon_tab.png")

	time.sleep(1)
	clickB10()

	#Check if a refill is necessary
	pos3 = imagesearch("./images/shop.png")
	if(pos3[0] != -1):
		search("./images/shop.png")
		time.sleep(1)
		search("./images/recharge.png")
		time.sleep(0.5)

		#check for the quiz.
		quiz_pos = imagesearch('./images/quiz.png')
		if(quiz_pos[0] != -1):
			pyautogui.screenshot("quiz" + str(screenshot_quiz) + ".png")
			screenshot_quiz = screenshot_quiz + 1
			restart(mode)

		search("./images/yes-recharge.png")
		time.sleep(1)
		search("./images/ok.png")
		search("./images/close.png")
		clickB10()
		search("./images/start.png")
	else:
		search("./images/start.png")

	time.sleep(10)

	if(mode == 1):
		search("./images/autoplay_button_gb10.png")
	elif(mode == 4):
		search("./images/autoplay_button_nb10.png")
	elif(mode == 5):
		search("./images/autoplay_button_db10.png")

	print("Restart Command Ended.")

def checkSlot(image_directory , slot_num):
	slot_pos = imagesearch(image_directory)
	if(slot_pos[0] != -1):
		print("Slot " + str(slot_num))
		return slot_num
	else:
		return -1

'''
Detects and returns the rune slot number.
'''
def detectRuneSlot():
	slot_num = -1
	counter = 1

	while(counter < 7):
		image_directory = './images/rune/slot_' + str(counter) + '.png'
		slot_num = checkSlot(image_directory, counter)
		if(slot_num != -1):
			return slot_num
		else:
			counter = counter + 1


def getRuneStats():
	# load the example image and convert it to grayscale
	image = cv2.imread('./screenshots/123.png')

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#gray = cv2.GaussianBlur(gray, (5,5), 0)
	gray = cv2.medianBlur(gray, 3)

	#kernel = np.ones((5, 5), np.uint8)
	#cv2.dilate(im, kernel, iterations = 1)
	#cv2.erode(gray, kernel, iterations = 1)

	
	#gray = cv2.bilateralFilter(gray,9,75,75)
	#gray = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)

	#scale = 2.5
	#width = int(gray.shape[1] * scale)
	#height = int(gray.shape[0] * scale )
	#dim = (width, height)

	#gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)


	gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

	# write the grayscale image to disk as a temporary file so we can apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	print(text)

	cv2.imshow("Output", gray)
	cv2.waitKey(0)

def hasSPD():
	start = imagesearch('./images/rune/set/swift_2.png')
	end = imagesearch('./images/ok.png')

	#print (start)
	#print (end)
	
	aoi = imagesearcharea('./images/rune/spd.png', start[0]-220, start[1], end[0], end[1]-75)

	if(aoi[0] != -1):
		#im = pyautogui.screenshot(region=(aoi[0],aoi[1],end[0],end[1]))
		#im.save("sublocation.png")
		#print(aoi)
		return True
	else:
		#print("SPD sub not found.")
		return False

def isRuneType(rune_type):
	if(rune_type == "swift"):
		pos = imagesearch('./images/rune/set/swift_2.png')
	elif(rune_type == "energy"):
		pos = imagesearch('./images/rune/set/energy.png')
	elif(rune_type == "blade"):
		pos = imagesearch('./images/rune/set/blade.png')
	elif(rune_type == "despair"):
		pos = imagesearch('./images/rune/set/despair.png')
	elif(rune_type == "fatal"):
		pos = imagesearch('./images/rune/set/fatal.png')
	else:
		print ("Unknown Rune Type.")

	if(pos[0] != -1):
		return True
	else:
		return False


def dimensionalRiftBypass():
	ok_pos = imagesearch('./images/ok.png')
	if(ok_pos != -1):
		search('./images/ok.png')
		search('./images/reverse.png')
		search('./images/battle_icon.png')
		time.sleep(10)
		search('./images/cairos_dungeon.png')
		time.sleep(2)




def autoBattle(refill_counter,max_counter):
	
	auto_battle_active = 1

	currentTime = datetime.now()
	ct_string = currentTime.strftime("%d-%m-%H-%M-%S")

	while(auto_battle_active == 1):
		#check for replay button.
		change = imagesearch('./images/auto battle/replay.png')

		if(change[0] != -1):
			search('./images/auto battle/replay.png')
			search('./images/auto battle/repeat_battle.png')
			check = search('./images/auto battle/shop.png')

			if(max_counter > refill_counter):
				if(check != -1):
					search('./images/auto battle/recharge_energy_190.png')

					#INSERT QUIZ BYPASS HERE.
					quiz_check = search('./images/auto battle/quiz.png')
					if(quiz_check != -1):
						pyautogui.screenshot("./screenshots/quiz data/" + ct_string + ".png")
						print("Quiz Detected.")
						sys.ext()

					search('./images/auto battle/yes.png')
					search('./images/auto battle/ok.png')
					search('./images/auto battle/close.png')
					search('./images/auto battle/repeat_battle.png')
					refill_counter = refill_counter + 1
					print("Current Refill: " + str(refill_counter))
			else:
				auto_battle_active = 2
				print("Desired Refill has been reached. Program Ended.")
				sys.ext()

def quizSolver():
	search('./images/sw_tab.png')
	search('./images/sw_close.png')
	print("quiz solver to be added.")





	







