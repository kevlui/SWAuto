from auto import *
import sys
import time 
import argparse


try:
	counter = 1
	refill = 0
	screenshot_counter = 0
	screenshot_quiz = 0
	mode = 0


	# -n: number of refills 
	# -d: dungeon type (gb,db,nb)

	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num', dest = "refills", default = 10 , type = int)
	parser.add_argument('-d', '--dungeon', dest = "dungeon" , default= "gb")
	args = parser.parse_args()

	if(args.dungeon == "gb"):
		print("GB10 Selected.")
	elif(args.dungeon == "db"):
		print("DB10 Selected.")
	elif(args.dungeon == 'nb'):
		print("NB10 Selected.")
	elif(args.dungeon == 'toa'):
		print("Toa Selected.")
	elif(args.dungeon == 'erift'):
		print("Elemental Rift Detected.")
		mode = 2
	elif(args.dungeon == 'drift'):
		print("Elemental Rift Detected.")
		mode = 3
	else:
		print("Not a dungeon option. Please input gb, db, nb for your desired dungeon type.")

	print ("Number of refills: " + str(args.refills))
	mod_refill = args.refills + 1


	while(refill < mod_refill):
		conditional = -1
		pos = [-1,-1]
		pos2 = [-1,-1]

		#Search for successful or failed run.
		while(conditional == -1):
			if(mode == 2):
				pos = imagesearch("./images/result.png")
			else:
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

			if(mode == 2):
				time.sleep(3)
				click_image("./images/result.png", pos, "left", 0.2, offset=5)
				time.sleep(0.5)
				click_image("./images/result.png", pos, "left", 0.2, offset=5)
				time.sleep(2)
				search("./images/ok-erift.png")
			else:
				click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)
				time.sleep(0.5)
				click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)
				time.sleep(1)


				#INSERT RUNE CHECKING STUFF HERE
				sell_pos = imagesearch("./images/sell.png")
				if(sell_pos[0] != -1):
					rune_pos = imagesearch("./images/sixstar.png",0.9)
					if(rune_pos[0] != -1):
						pyautogui.screenshot("./screenshots/6/" + str(screenshot_counter) + ".png")
						search("./images/ok.png")
					else:
						if(isRuneType("swift")):
							search("./images/ok.png")						
						else:
							search("./images/sell.png")
							search("./images/yes-sell.png")
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

			#Check if the desired number of refill is hit.
			refill = refill + 1	
			if(refill == mod_refill):
				print("End of Script.")
				sys.exit()

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
			else:
				print("Refill: " + str(refill))
				search("./images/yes-recharge.png")
				time.sleep(1)
				search("./images/ok.png")
				time.sleep(1)
				search("./images/close.png")
				time.sleep(1)
			if conditional == 1:
				search("./images/replay.png")

			elif conditional == 2:
				search("./images/prepare-failed.png")
		
		#Need to click start if the run failed.
		if conditional == 2:
			search("./images/start.png")

			if(mode == 3):
				search("./images/start_drift.png")


		time.sleep(1)
	counter = counter + 1

except KeyboardInterrupt:	
	print("Keyboard Interrupt")