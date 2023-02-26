import time 
import pyautogui
import sys
from imagesearch import *
from datetime import datetime
import os
import random
import logging 

import cv2
import numpy as np
import pandas as pd

import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'.\hello tess\tesseract.exe'

#
def findText(imgPath):
    #pyautogui.screenshot("./text_read.png")
    img = cv2.imread(imgPath)

    #data = pytesseract.image_to_data(img, output_type='dict')
    data = pytesseract.image_to_string(imgPath)
    #print(data)
    return data
    
    # boxes = len(data['level'])
    # for i in range(boxes ):
    #     (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    #     #print(str(x) + str(y) + str(w) + str(h))
    #     #Draw box        
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


#----- DRAWING RELATED METHODS-----
def sellRunes():
    #Search for the colors.
    blue_items = findColor()
    print("Blue Items Detected: ", blue_items)
    runes =[]

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    #Search for any 6-stars
    for item in blue_items:
        img = cv2.imread("./images/auto battle/dummy_rune.png")
        height, width, channels = img.shape

        topx = item[0] - 15
        topy = item[1] - height - 10
        botx = item[0] + width
        boty = item[1] + height

        screenshot = cv2.rectangle(screenshot, (topx,topy), (botx,boty), (0,255,0) , 3)
        target = imagesearcharea("./images/auto battle/star.png",topx,topy,botx,boty, 0.7)

        if(target[0] != -1):
            runes.append(item)


    if(len(runes) != 0):
        search("./images/auto battle/sell_selected.png")

        for item in runes:
            click_image("./images/auto battle/dummy_rune.png", item, "left", 0.2, offset=5)

        searchFix("./images/auto battle/sell.png", "./images/auto battle/yes_sell.png", True )
        searchFix("./images/auto battle/yes_sell.png", "./images/auto battle/yes_sell.png", False)

    print("Runes:", runes)
    return runes
        
def findColor():
    pyautogui.screenshot("./rune_selector.png")
    img = cv2.imread("./rune_selector.png")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(img,img, mask= mask)


    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    targets = []
    counter = 0

    topLeft = quizSearch("./images/auto battle/rune_top_left.png")
    botRight = quizSearch("./images/auto battle/sell_selected.png")

    print("topLeft: ", topLeft)
    print("botRight: ", botRight)

    #Searching for Blue runes.
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        
        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            coords = [x,y]

            #Filter out the ones not in the area.
            mana_icon = cv2.imread("./images/auto battle/rune_top_left.png")
            mana_height, mana_width, mana_channels = mana_icon.shape

            sell_button = cv2.imread("./images/auto battle/sell_selected.png")
            height, width, channels = sell_button.shape

            #item_area = cv2.imread("./images/auto_battle/dummy_rune.png")
            #item_height, item_width, item_channels = item_area.shape


            range_x = range(topLeft[0], botRight[0] + int(width))
            range_y = range(topLeft[1] + int(mana_height), botRight[1])

            if( (x in range_x) and (y in range_y)):
                #Filter out any blues within the same item area.
                if(containsDupe(coords, targets, 80 ) == False):
                    img = cv2.rectangle(img, (x, y), 
                                        (x + w, y + h), 
                                        (255, 0, 0), 2) 
                    cv2.putText(img, str(counter), (x, y), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.0, (255, 255, 255)) 
                    targets.append(coords)

            
            #print(counter, coords)
            counter = counter + 1

    #print("Targets: ", targets)
    cv2.imwrite('ztest.jpg', img)
    return targets
    #cv2.imwrite('frame.jpg', img)
    #cv2.imwrite('zmask.jpg',mask)
    #cv2.imwrite('zres.jpg',res)


#----- DEBUG METHODS --------
def quizSearch(image_directory):
    delay = random.randint(1,2)
    button = imagesearch(image_directory,0.7)
    if button[0] != -1:
        #print("FOUND: " + image_directory)
        return button
    else:
        #print( image_directory + "not found.")
        return -1

def displayTarget(buttons,name):
    img = pyautogui.screenshot()
    img = np.array(img)

    print('buttons:', buttons)

    for button in buttons:
        image = cv2.rectangle(img, button, (button[0]+20,button[1]+20), (0,255,0) , 3)

    #cv2.imshow("target_map", image)
    cv2.imwrite(name, image)
    #k = cv2.waitKey(0) # 0==wait forever

#-----------HELPER METHODS-------------


def search(image_directory):
    delay = random.randint(2,3)
    time.sleep(delay)
    button = imagesearch(image_directory)
    #now = datetime.now
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if button[0] != -1:
        print(" Found " + image_directory)
        logging.info("Clicking " +  image_directory)
        click_image(image_directory, button, "left", 0.2, offset=5)
        return button
    else:
        print(" Not Found " + image_directory)
        logging.info(image_directory + " is not found")
        return -1

# check_image = TRUE if you want the image next_image to be present. FALSE if you want the next one to be gone.    
def searchFix(image_directory, next_image_directory, check_image, modifiedDelay=10):
    
    failCounter = 0

    while(failCounter < 10):
        delay = random.randint(4,5)
        button = imagesearch(image_directory)

        if (button[0] != -1):
            print(" Found " + image_directory)
            time.sleep(delay)
            click_image(image_directory, button, "left", 1, offset=5)
            print("Clicking " +  image_directory)
            time.sleep(delay)

            #account for any vm lags - if the button is still there, keep clicking.

            #Check if the following image is there as intended.
            checkImageNum = 0
            clickCounter = 0

            while(clickCounter < 1):
                while(checkImageNum < modifiedDelay):
                    checkLag = imagesearch(next_image_directory)

                    #Random click to force reset the screen.
                    #pyautogui.moveTo(385,783, 2, pyautogui.easeInQuad)
                    #pyautogui.click()

                    #If image is intended to found BUT not found:
                    if (check_image == True) and (checkLag[0] == -1):
                        print("Stalling Detected: Cannot find " + next_image_directory)
                        print('Current CheckImage Num: ' + str(checkImageNum))
                        checkImageNum = checkImageNum + 1
                        pyautogui.moveTo(385,783, 2, pyautogui.easeInQuad)
                        pyautogui.click()
                        time.sleep(2)

                    #If image is intended to be not found BUT found:
                    elif (check_image == False) and (checkLag[0] != -1):
                        print("Stalling Detected: Following image detected " + next_image_directory )
                        print('Current CheckImage Num: ' + str(checkImageNum))
                        checkImageNum = checkImageNum + 1
                        pyautogui.moveTo(385,783, 2, pyautogui.easeInQuad)
                        pyautogui.click()
                        time.sleep(2)
                    else:
                        print("Stalling Ended.")
                        checkImageNum = modifiedDelay + 1

                #If the scan completed and the intended state is incorrect:
                if(checkImageNum == modifiedDelay):
                    print("Clicking: " + image_directory)
                    click_image(image_directory, button, "left", 0.2, offset=5)
                    clickCounter = clickCounter + 1
                else:
                    clickCounter = 5
                    failCounter = 100

            if(clickCounter == 3):
                sys.ext("Stall Timer exceeded. Program ending.")

        else:
            print(" Not Found " + image_directory)
            logging.info(image_directory + " is not found")
            print("Retrying to find: ", image_directory)
            failCounter = failCounter + 1

            if(failCounter > 5):
                sys.ext("Fail Counter exceeded. Program ending.")

def searchFixMulti(image_directory, next_image_directory, check_image, modifiedDelay=10):
    print('Method for Search Fix if there are multiple next_image_outcomes')

def search_loop(image_directory):
    search_bool = 0
    while(search_bool != 1):
        search_pos = imagesearch(image_directory)
        if(search_pos[0] != -1):
            search(image_directory)
            search_bool = 1

def searchFixLoop(image_chain):
    max_length = len(image_chain)
    current = 0

    while (current < max_length):
        searchFix(image_chain[current][0], image_chain[current + 1][0], image_chain[current][1])
        current = current + 1
    
    searchFix(image_chain[current][0], image_chain[current][0], image_chain[current][1])


#---------SW METHODS------------------

def dimensionalRiftBypass():
    ok_pos = imagesearch('./images/ok.png')
    if(ok_pos != -1):
        search('./images/ok.png')
        search('./images/reverse.png')
        search('./images/battle_icon.png')
        time.sleep(10)
        search('./images/cairos_dungeon.png')
        time.sleep(2)

def checkLost(counter):
    button = imagesearch('./images/auto battle/lose.png')
    if button[0] != -1:
        counter = counter + 1
        print("Lost Battle Detected. Current Fails: " + str(counter))
        logging.info("Lost Battle Detected. Current Fails: " + str(counter))
        return counter
    else:
        logging.info("Lost Battle not Detected.")
        return counter

def autoBattle(refill_counter,max_counter):
    auto_battle_active = 1
    num_lost = 0

    while(auto_battle_active == 1):
        #check for replay button.
        change = imagesearch('./images/auto battle/replay.png')

        if(change[0] != -1):

            #Clear out the unwanted runes.
            runes = sellRunes()
            num_lost = checkLost(num_lost)
            time.sleep(2)


            #Deal with the would you like to sort your rewards thing.
            if(len(runes) != 0):
                searchFix('./images/auto battle/replay.png','./images/auto battle/repeat_battle.png', True, 8)
            else:
                #If no runes dropped, - the rewards check dialog doesnt pop.
                search('./images/auto battle/replay.png')
                rewardsDialog = imagesearch('./images/auto battle/yes-replay.png')

                #If the dialog shows up, press yes.
                if(rewardsDialog != -1):
                    searchFix('./images/auto battle/yes-replay.png','./images/auto battle/yes-replay.png', False,8)


            search('./images/auto battle/repeat_battle.png')

            #Check if it the repeat-battle has stalled.
            time.sleep(2)
            checkStall = imagesearch('./images/auto battle/sell_selected.png')
            checkShop = imagesearch('./images/auto battle/shop.png')
            print("checkStall: ", checkStall)
            print("checkShop: ", checkShop)

            #if the shop and autobattling is not found, it has stalled so it needs to be clicked again.
            while ((checkStall[0] == -1) and (checkShop[0] == -1)):
                print("Stalling detected for repeat_battle.png")
                search('./images/auto battle/repeat_battle.png')
                time.sleep(1)
                checkStall = imagesearch('./images/auto battle/sell_selected.png')
                checkShop = imagesearch('./images/auto battle/shop.png')


            time.sleep(3)
            check = imagesearch('./images/auto battle/shop.png')

            #Check if there is a prompt after clicking repeat battle.
            
            '''
            rune_full = imagesearch('./images/auto battle/yes-rune.png')
            if(rune_full != -1):
                print("Runes are filled. Ending program.")
                sys.ext()
            '''

            #Check for the refill option.
            if(max_counter > refill_counter):
                if(check[0] != -1):
                    print("Shop Detected - Refilling...")
                    searchFix('./images/auto battle/shop.png', './images/auto battle/shop.png', False)
                    time.sleep(2)
                    searchFix('./images/auto battle/recharge_energy_190.png', './images/auto battle/yes.png', True)

                    #Quiz Bypass
                    quiz_check = search('./images/auto battle/quiz.png')
                    if(quiz_check != -1):
                        logging.info("Quiz Detected.")
                        print("Quiz Detected.")
                        date = datetime.today()
                        pyautogui.screenshot("quiz_" + str(date) + ".png")
                        quizSolver()
                        searchFix('./images/auto battle/ok-quiz-submit.png', './images/auto battle/ok-quiz-correct.png', True)
                        searchFix('./images/auto battle/ok-quiz-correct.png', './images/auto battle/ok-quiz-correct.png', False)
                        


                    searchFix('./images/auto battle/yes.png', './images/auto battle/ok_confirm.png', True)
                    searchFix('./images/auto battle/ok_purchase.png', './images/auto battle/ok_purchase.png', False)
                    searchFix('./images/auto battle/close-shop.png', './images/auto battle/repeat_battle.png', True )
                    searchFix('./images/auto battle/repeat_battle.png', './images/auto battle/repeat_battle.png', False )

            else:
                auto_battle_active = 2
                print("Desired Refill has been reached. Program Ended.")
                sys.ext()

def toa():
    """
    search("./images/victory-paint.png")
    search("./images/victory-paint.png")
    search("./images/ok.png")	
    search("./images/next_stage.png")
    search("./images/start.png")
    """
    searchFix("./images/victory-paint.png","./images/ok.png", True)
    searchFix("./images/ok.png","./images/next_stage.png", True)
    searchFix("./images/next_stage.png","./images/start.png", True)
    searchFix("./images/start.png","./images/start.png", False)


#---- QUIZ SOLVER RELATED -----
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

    currentTime = datetime.now()
    ct_string = currentTime.strftime("%d-%m-%H-%M-%S")
    pyautogui.screenshot("./screenshots/quiz data/" + ct_string + ".png")

    if(target_info[1] == "Boss"):
        files = absoluteFilePaths('./Captcha Images/Boss')
    elif(target_info[1] == "Ellia"):
        files = absoluteFilePaths('./Captcha Images/Ellia')
    elif(target_info[1] == "Rocks"):
        files = absoluteFilePaths('./Captcha Images/Rocks')
    elif(target_info[1] == "Trees"):
        files = absoluteFilePaths('./Captcha Images/Trees')
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


        displayTarget(monsters,"./quiz_solver/quiz_mons" + ct_string + ".jpg")


    else:
        for button in buttons:
            click_image('./Captcha Images/Boss/dragon.png', button, "left", 0.2, offset=5)
            time.sleep(2)

        displayTarget(buttons, "./quiz_solver/quiz_buttons" + ct_string + ".jpg")

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
    displayTarget(mapLocations, "quiz_click_locations.jpg")
    return mapLocations




    







