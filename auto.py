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

def restart():
	search('./images/sw_tab.png')
	time.sleep(0.5)
	search('./images/sw_close.png')
	search('./images/sw_icon.png')

	restart = -1

	while(restart == -1):
		start_pos = imagesearch('./images/touch_to_start.png')
		if(start_pos[0] != -1):
			restart = 0

	search('./images/touch_to_start.png')

	ad = 0

	#Check for adds and close them.
	while(ad < 5):
		start_ad_pos = imagesearch('./images/start_ad_close.png')
		if(start_ad_pos[0] != -1):
			search('./images/start_ad_close.png')
			ad = ad + 1
		else:
			ad = 10

	search('./images/sw_intro_skip.png')

	time.sleep(2)
	search('./images/ad_close_2.png')
	time.sleep(.5)
	search('./images/ad_close_3.png')
	time.sleep(2)

	search('./images/battle_icon.png')
	time.sleep(2)
	search('./images/cairos_dungeon.png')

	time.sleep(2)
	search('./images/start_battle_screen.png')
	search("./images/start.png")

	autoplay = 0
	while(autoplay != 1):
		autoplay_pos = imagesearch("./images/autoplay_button_gb10.png")
		if(autoplay_pos[0] != -1):
			search("./images/autoplay_button_gb10.png")
			autoplay = 1

	print("Restart Command Ended.")


try:
	counter = 1
	refill = 0
	screenshot_counter = 0


	while(refill < 10):
		conditional = -1
		pos = [-1,-1]
		pos2 = [-1,-1]

		#Search for successful or failed run.
		while(conditional == -1):
			pos = imagesearch("./images/victory-paint.png")
			pos2 = imagesearch("./images/no.png")
				
			if(pos[0] != -1):			#If Victory img is found
				conditional = 1
			elif(pos2[0] != -1):		#If Fail is found.
				conditional = 2

		#If run is successful:
		if(conditional == 1):
			print("Run successful: " + str(counter))
			time.sleep(3)
			click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)
			time.sleep(0.5)
			click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)

			time.sleep(1)
			#INSERT RUNE CHECKING STUFF HERE
			sell_pos = imagesearch("./images/sell.png")
			if(sell_pos[0] != -1):
				rune_pos = imagesearch("./images/sixstar.png",0.9)
				if(rune_pos[0] != -1):
					#print("Rune is 6-starred.")
					pyautogui.screenshot("./screenshots/6/" + str(screenshot_counter) + ".png")
					search("./images/ok.png")
				else:
					#print("Rine is 5-starred.")
					pyautogui.screenshot("./screenshots/5/" + str(screenshot_counter) + ".png")
					search("./images/sell.png")
					search("./images/yes-sell.png")
					#search("./images/ok.png")
			else:
				search("./images/ok.png")
			
			search("./images/replay.png")
			counter = counter + 1
			screenshot_counter = screenshot_counter + 1
		#IF run fails:
		elif(conditional == 2):
			print("Run failed.")
			
			search("./images/no.png")
			time.sleep(2)
			pyautogui.click(button='left')

			search("./images/prepare-failed.png")

		#Check if refill is neccessary
		time.sleep(1)
		pos3 = imagesearch("./images/shop.png")
		if(pos3[0] != -1):
			search("./images/shop.png")
			time.sleep(1)
			search("./images/recharge.png")
			time.sleep(0.5)

			#check for the quiz.
			quiz_pos = imagesearch('./images/quiz.png')
			if(quiz_pos[0] != -1):
				pyautogui.screenshot("quiz.png")
				restart()

			search("./images/yes-recharge.png")
			search("./images/ok.png")
			search("./images/close.png")
			refill = refill + 1
			print("Refill: " + str(refill))

			if conditional == 1:
				search("./images/replay.png")

			elif conditional == 2:
				search("./images/prepare-failed.png")
		
		#Need to click start if the run failed.
		if conditional == 2:
			search("./images/start.png")


		time.sleep(1)
	counter = counter + 1

except KeyboardInterrupt:	
	print("Keyboard Interrupt")


