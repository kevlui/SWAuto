import time 
import pyautogui
import sys
from imagesearch import *


def search(image_directory):
	time.sleep(1)
	button = imagesearch(image_directory)
	if button[0] != -1:
		click_image(image_directory, button, "left", 0.2, offset=5)
	else:
		print(image_directory + "is not found")

def search_loop(image_directory):
	search_bool = 0
	while(search_bool != 1):
		search_pos = imagesearch(image_directory)
		if(search_pos[0] != -1):
			search(image_directory)
			search_bool = 1

def restart():
	#Restart the application
	search('./images/sw_tab.png')
	time.sleep(0.5)
	search('./images/sw_close.png')
	search('./images/sw_icon.png')

	#Check for "Touch to start"
	restart = -1
	while(restart == -1):
		start_pos = imagesearch('./images/touch_to_start.png')
		if(start_pos[0] != -1):
			restart = 0

	time.sleep(3)

	#Check for adds and close them.
	ad = 0
	while(ad < 5):
		start_ad_pos = imagesearch('./images/start_ad_close.png')
		if(start_ad_pos[0] != -1):
			search('./images/start_ad_close.png')
			ad = ad + 1
		else:
			ad = 10

	search('./images/touch_to_start.png')

	time.sleep(2)
	search('./images/sw_intro_skip.png')

	time.sleep(2)
	search('./images/ad_close_2.png')
	time.sleep(.5)
	search('./images/ad_close_3.png')
	time.sleep(5)

	search('./images/battle_icon.png')
	time.sleep(2)
	search('./images/cairos_dungeon.png')
	time.sleep(2)

	imagesearch_loop('./images/gb10_icon.png',1)
	time.sleep(2)
	search('./images/start_battle_screen.png')
	time.sleep(2)

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
			restart()

		search("./images/yes-recharge.png")
		search("./images/ok.png")
		search("./images/close.png")
		search('./images/start_battle_screen.png')
		time.sleep(1)
		search("./images/start.png")
	else:
		search("./images/start.png")

	autoplay = 0
	while(autoplay != 1):
		autoplay_pos = imagesearch("./images/autoplay_button_gb10.png")
		if(autoplay_pos[0] != -1):
			search("./images/autoplay_button_gb10.png")
			autoplay = 1

	print("Restart Command Ended.")

def restart2():
	search('./images/cairos_dungeon.png')
	time.sleep(2)

	imagesearch_loop('./images/gb10_icon.png',1)
	time.sleep(2)
	search('./images/start_battle_screen.png')
	time.sleep(2)





