from auto import *
import sys
import time 
import argparse
from imagesearch import *

try:
	counter = 1
	refill = 0
	screenshot_counter = 0
	screenshot_quiz = 0
	mode = 0


	# -n: number of refills 
	# -d: dungeon type (gb,db,nb)

	logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w') 
	logger=logging.getLogger() 
	logger.setLevel(logging.DEBUG) 

	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num', dest = "refills", default = 0 , type = int)
	parser.add_argument('-d', '--dungeon', dest = "dungeon" , default= "gb")
	args = parser.parse_args()

	if(args.dungeon == "gb"):
		print("GB10 Selected.")
		mode = 1
	elif(args.dungeon == "db"):
		print("DB10 Selected.")
		mode = 5
	elif(args.dungeon == 'nb'):
		print("NB10 Selected.")
		mode = 4
	elif(args.dungeon == 'toa'):
		print("Toa Selected.")
		mode = 6
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

	print("7th Anniversary Patch")


	while(refill < mod_refill):
		conditional = -1
		pos = [-1,-1]
		pos2 = [-1,-1]

		#Search for successful or failed run.
		while(conditional == -1):
			if(mode == 2):
				pos = imagesearch("./images/result.png")
				print("Victory Detected.")
			else:
				pos = imagesearch("./images/victory-paint.png")

			pos2 = imagesearch("./images/no.png")
				
			if(pos[0] != -1):			#If Victory img is found
				conditional = 1
				print(conditional)
			elif(pos2[0] != -1):		#If Fail is found.
				conditional = 2

		#If run is successful:
		if(conditional == 1):
			print("Run successful: " + str(counter))
			time.sleep(3)

			if(mode == 6 ):
				click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)
				click_image("./images/victory-paint.png", pos, "left", 0.2, offset=5)
				search("./images/ok.png")	
				search("./images/next_stage.png")
				search("./images/start.png")


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
					rune_pos2 = imagesearch("./images/sixstar_2.png",0.9)
					rune_boolean = -1

					#if(rune_pos[0] != -1):
					#	pyautogui.screenshot("./screenshots/6/" + str(screenshot_counter) + ".png")
					#	search("./images/ok.png")

					if(rune_pos[0] != -1):
						rune_boolean = 1
					elif(rune_pos2[0] != -1):
						rune_boolean = 2

					#6-STARS
					currentTime = datetime.now()
					ct_string = currentTime.strftime("%d-%m-%H-%M-%S")

					if((rune_boolean == 1) or (rune_boolean == 2)):
						print("keeping rune.")
						pyautogui.screenshot("./screenshots/keep/" + ct_string + ".png")
						search("./images/ok.png")
					else:
						if(isRuneType("swift")):
							if(checkSlot("./images/rune/slot_2.png",2) == 2):
								pyautogui.screenshot("./screenshots/discard/" + ct_string + ".png")
								search("./images/sell.png")
								search("./images/yes-sell.png")
								#search("./images/ok.png")
							else:
								if(hasSPD()):
									pyautogui.screenshot("./screenshots/keep/" + ct_string + ".png")
								else:
									pyautogui.screenshot("./screenshots/discard/" + ct_string + ".png")
								search("./images/ok.png")						
						else:
							print("selling rune.")
							pyautogui.screenshot("./screenshots/discard/" + ct_string + ".png")
							search("./images/sell.png")
							search("./images/yes-sell.png")
							#search("./images/ok.png")
				else:
					search("./images/ok.png")

			#EVENT-ONLY DROPS CHECKING.
			print("Checking Event Drop" )

			if(search("./images/replay.png") == -1):
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
		print("checking refill")
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
				restart(mode)
			else:
				print("Refill: " + str(refill))
				search("./images/yes-recharge.png")
				time.sleep(1)
				search("./images/ok-2.png")
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
	print("next loop.")

except KeyboardInterrupt:
	print("Keyboard Interrupt")
