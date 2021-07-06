import pytesseract
import pyautogui
import os
from imagesearch import *
from auto import *

pytesseract.pytesseract.tesseract_cmd = r'.\hello tess\tesseract.exe'


def absoluteFilePaths(directory):
	file_paths = []

	for root,dirs,files in os.walk(directory):
		for file in files:
			p = os.path.join(root,file)
			file_paths.append(os.path.abspath(p))
			#print(os.path.abspath(p))

	return file_paths


def parseQuiz(image_directory):
	img_text = pytesseract.image_to_string(image_directory)
	img_text2 = img_text.replace('\n'," ")
	word_list = img_text2.split(" ")
	#print(word_list)


	#Find the start and end of the directions string.
	counter = 0
	start = 0
	end = 0

	for word in word_list:
		if (word == 'Select'):
			start = counter
		elif (word == 'total)'):
			end = counter

		counter += 1

	#Get the directions in the quiz.
	directionString = word_list[slice(start,end+1)]


	#Get the total number of pictures for target
	total = word_list[slice(end-2,end+1)]
	count = total[0]
	count = int(count[1:])
	print(count)


	#Find the target.
	target = directionString[2]
	print("Target is: " + target)

	return [count,target]
	

def containsDupe(target, array, margin):
	for current in array:
		range_x = range(current[0]-margin, current[0]+margin)
		range_y = range(current[1]-margin, current[1]+ margin)
		if (target[0] in range_x) and (target[1] in range_y):
			return True
	return False


def quizSolver():
	img = pyautogui.screenshot()
	target_info = parseQuiz(img)
	print("\n")

	if(target_info[1] == "Boss"):
		files = absoluteFilePaths('./Captcha Images/Boss')
	elif(target_info[1] == "Ellia"):
		files = absoluteFilePaths('./Captcha Images/Ellia')
	else:
		files_boss = absoluteFilePaths('./Captcha Images/Boss')
		files_ellia = absoluteFilePaths('./Captcha Images/Ellia')
		files = files_boss + files_ellia

	buttons = []

	for file in files:
		button = quizSearch(file)
		if button != -1:
			print(button)
			if containsDupe(button,buttons,10) == False:
				buttons.append(button)

	if(target_info[1] == "Monsters"):
		monsters = []
		mapLocations = mapAnswers(55,55)

		for location in mapLocations:
			if(containsDupe(location,buttons, 50) == False):
				monsters.append(location)

		#Click each monster
		for monster in monsters:
			click_image('./Captcha Images/Boss/dragon.png', monster, "left", 0.2, offset=5)
			time.sleep(2)

		#displayTarget(monsters)

	else:
		for button in buttons:
			click_image('./Captcha Images/Boss/dragon.png', button, "left", 0.2, offset=5)
			time.sleep(2)

		#displayTarget(buttons)

def mapAnswers(margin_x, margin_y):
	mapLocations = []
	buttons = []

	glass = quizSearch('./Captcha Images/hourglass.png')
	ok = quizSearch('./Captcha Images/ok.png')


	x_increment = (glass[0] - ok[0])/2
	y_increment = (glass[1] - ok[1])/2
	counter = 0
	increment = 1

	#Build out the top row
	while(counter != 4):
		y = glass[1] + margin_y
		x = ok[0] + (increment * x_increment) + margin_x
		point = (int(x), int(y))

		counter = counter + 1
		increment = increment - 1

		mapLocations.append(point)

	counter = 0
	increment = 1
	#Build out the lower row:
	while(counter != 4):
		y = ok[1] + y_increment + margin_y
		x = ok[0] + (increment * x_increment) + margin_x
		point = (int(x), int(y))

		counter = counter + 1
		increment = increment - 1
		mapLocations.append(point)

	buttons.append(glass)
	buttons.append(ok)

	#displayTarget(buttons)
	#displayTarget(mapLocations)
	return mapLocations