import time 
import pyautogui
import cv2 as cv2
import random
from auto import *
from imagesearch import *
import logging 
import argparse


def sellTest():
    blue_items = findColor()
    print("Blue Items Detected: ", blue_items)
    runes = []

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

        print("target:", target)
        if(target[0] != -1):
            runes.append(target)


    cv2.imwrite("sellTestScreenShot.png", screenshot)


def autoToa():
    print('Auto Toah Starting...')
    test = 0

    while(test == 0):
        victory = imagesearch('./images/victory-paint.png')

        if(victory[0] != -1):
            time.sleep(10)
            victory2 = imagesearch('./images/victory-paint.png')

            if(victory2[0] != -1):
                search('./images/victory-paint.png')
                time.sleep(2)
                search('./images/victory-paint.png')
                time.sleep(2)
                search('./images/toa-ok.png')
                time.sleep(2)
                search('./images/next_stage.png')
                time.sleep(2)
                search('./images/auto_play.png')
            

def replay():
    search("./images/auto battle/sell_selected.png")
    search("./images/auto battle/sell_selected_reg.png")
    search("./images/auto battle/yes_sell_rune.png")

    search("./images/auto battle/nothing_sell_ok.png")
    search("./images/auto battle/nothing_sell_cancel.png")

    #Check if the warning for the legend is there:
    search("./images/auto battle/yes_sell_legend.png")

    search("./images/auto battle/replay.png")
    search("./images/auto battle/repeat_battle.png")

def replayFix():
    time.sleep(2)

    searchFix("./images/auto battle/sell_selected.png", "./images/auto battle/sell_selected_reg.png", True)
    
    searchFix("./images/auto battle/sell_selected_reg.png", "./images/auto battle/sell_all.png", True)
    #searchFix("./images/auto battle/sell_all.png", "./images/auto battle/sell_all.png", False)
    #search("./images/auto battle/sell_selected_reg.png")
    time.sleep(2)

    #noSell = imagesearch("./images/auto battle/nothing_sell_ok.png")
    sell = imagesearch("./images/auto battle/sell_runes.png")

    if(sell[0] == -1):
        print('Nothing to sell detected.')
        searchFix("./images/auto battle/nothing_sell_ok.png", "./images/auto battle/nothing_sell_ok.png", False)
        searchFix("./images/auto battle/nothing_sell_cancel.png", "./images/auto battle/nothing_sell_cancel.png", False)
        searchFix("./images/auto battle/replay.png", "./images/auto battle/replay.png", False)
    else:
        print('Sell Detected')
        search("./images/auto battle/sell_all.png")
        legendSell = imagesearch("./images/auto battle/yes_sell_legend.png")
        if(legendSell[0] != -1):
            search("./images/auto battle/yes_sell_legend.png")
        searchFix("./images/auto battle/replay.png", "./images/auto battle/replay.png", False)

    #time.sleep(3)
    #searchFix("./images/auto battle/repeat_battle.png", "./images/auto battle/repeat_battle.png", False)
    #search("./images/auto battle/repeat_battle.png")

def refill():
    time.sleep(2)
    search("./images/auto battle/refill_shop.png")
    search("./images/auto battle/recharge_energy_190.png")

    #Check for Quiz
    quiz_check = search('./images/auto battle/quiz.png')
    if(quiz_check != -1):
        logging.info("Quiz Detected.")
        print("Quiz Detected.")
        pyautogui.screenshot("quiz.png")
        quizSolver()
        searchFix('./images/auto battle/ok-quiz-submit.png', './images/auto battle/ok-quiz-correct.png', True)
        searchFix('./images/auto battle/ok-quiz-correct.png', './images/auto battle/ok-quiz-correct.png', False)
        
    search("./images/auto battle/yes_shop.png")
    search("./images/auto battle/yes_shop_ok.png")
    search("./images/auto battle/close_shop.png")
    search("./images/auto battle/repeat_battle.png")

def refillFix():
    time.sleep(2)
    searchFix("./images/auto battle/refill_shop.png", "./images/auto battle/recharge_energy_190.png", True)
    searchFix("./images/auto battle/recharge_energy_190.png", "./images/auto battle/recharge_energy_190.png", False)

    #Check for Quiz
    quiz_check = search('./images/auto battle/quiz.png')
    if(quiz_check != -1):
        logging.info("Quiz Detected.")
        print("Quiz Detected.")
        pyautogui.screenshot("quiz.png")
        quizSolver()
        searchFix('./images/auto battle/ok-quiz-submit.png', './images/auto battle/ok-quiz-correct.png', True)
        searchFix('./images/auto battle/ok-quiz-correct.png', './images/auto battle/ok-quiz-correct.png', False)
        
    searchFix("./images/auto battle/yes_shop.png", "./images/auto battle/yes_shop_ok.png", True)
    searchFix("./images/auto battle/yes_shop_ok.png", "./images/auto battle/close_shop.png", True)
    searchFix("./images/auto battle/close_shop.png", "./images/auto battle/repeat_battle.png", True )
    searchFix("./images/auto battle/repeat_battle.png", "./images/auto battle/repeat_battle.png", False)

def refillUI():
    time.sleep(2)
    searchFix("./images/auto battle/refill_shop.png", "./images/auto battle/recharge_energy_190.png", True)
    searchFix("./images/auto battle/recharge_energy_190.png", "./images/auto battle/recharge_energy_190.png", False)

    #Check for Quiz
    quiz_check = search('./images/auto battle/quiz.png')
    if(quiz_check != -1):
        logging.info("Quiz Detected.")
        print("Quiz Detected.")
        pyautogui.screenshot("quiz.png")
        quizSolver()
        searchFix('./images/auto battle/ok-quiz-submit.png', './images/auto battle/ok-quiz-correct.png', True)
        searchFix('./images/auto battle/ok-quiz-correct.png', './images/auto battle/ok-quiz-correct.png', False)
        
    searchFix("./images/auto battle/yes_shop.png", "./images/auto battle/yes_shop_ok.png", True)
    searchFix("./images/auto battle/yes_shop_ok.png", "./images/auto battle/close_shop.png", True)
    searchFix("./images/auto battle/close_shop.png", "./images/auto battle/close_shop.png", False )
    
def testAuto():
    print('Testing...')
    current_refill = 0
    conditional = -1

    while(current_refill < 10):

        print('Waiting for Replay...')

        while(conditional == -1):
            pos = imagesearch("./images/auto battle/replay.png")
            #currentEnergy = refillFromScreen()
            time.sleep(5)
            if(pos[0] != -1):			#Battle has ended.
                print("Repeat Battle has ended. Replaying.")
                replayFix()

                print('Initial Repeat Battle.')
                search("./images/auto battle/repeat_battle.png")
                checkRefill = 0

                while(checkRefill == 0):
                    repeatBattleCheck = imagesearch("./images/auto battle/repeat_battle.png")
                    if repeatBattleCheck[0] != -1:
                        refill_pos = imagesearch("./images/auto battle/refill_shop.png")
                        repeatBattleCheck = imagesearch("./images/auto battle/repeat_battle.png")

                        if(refill_pos[0] != -1):
                            checkRefill = 1
                            print('Refill Required.')
                            refillFix()
                        elif(refill_pos[0]) == 0 and (repeatBattleCheck[0] != 0):
                            print('Re-trying to click repeat battle')
                            search("./images/auto battle/repeat_battle.png")
                        elif(repeatBattleCheck[0] == 0):
                            print('No repeat battle or refill found')	
                            checkRefill = 1
                    else:
                        print('Initial Repeat Battle Successful ... Ending loop.')
                        checkRefill = 1
                    time.sleep(2)
            # if(currentEnergy < 12):
            # 	print('Refill Required:  ' + str(currentEnergy))
            # 	searchFix('./images/refill/addEnergy.png', "./images/auto battle/refill_shop.png", True)
            # 	refillUI()

                
def test():
    refill_pos = imagesearch("./images/test.png")
    print('Checking if icon exists:' + str(refill_pos))


def refillFromScreen():
    energyPos = imagesearch('./images/refill/energy.png')
    addRefillPos = imagesearch('./images/refill/addEnergy.png')

    if(energyPos[0] != -1 and addRefillPos[0] != -1):
        pyautogui.screenshot('test-refill.png',region=(energyPos[0] + 50, energyPos[1], addRefillPos[0]-energyPos[0] - 40, 50 ))
        energyMeter = findText('test-refill.png')

        filteredString = ""

        for char in energyMeter:
            if(char.isdigit() or char == '/'):
                filteredString = filteredString + char
                
        currentEnergy = int(filteredString.split('/')[0])
        #print('Filtered String: ' + str(currentEnergy))
        return currentEnergy
    
    return 700

    
    

try:
    #autoToa()
    #test()
    #refillFromScreen()
    #testAuto()
    #getRuneText()
    left_corner = imagesearch('./images/rune_cleaner/mana_stone.png')
    bottom_corner = imagesearch('./images/rune_cleaner/sell_selected.png')

    #BGR
    lower_color = np.array([129, 50, 200])
    upper_color = np.array([158, 255, 255])

    if(left_corner[0] != -1 and bottom_corner[0] != -1):
        pyautogui.screenshot("./rune_selector.png", region=(left_corner[0], left_corner[1] + 40 , bottom_corner[0] - left_corner[0] + 220, 350))
        img = cv2.imread("./rune_selector.png")
        print('Screenshot Taken.')
        purpleLocations = findColor(img, lower_color, upper_color)


        rune_crafting_locations = imagesearch_occurances(img,'./images/rune_cleaner/rune_craft_purple.png')
        print(rune_crafting_locations)

        pyautogui.screenshot("./final_click_location.png")
        final_img = cv2.imread('./final_click_location.png')
        final_click = []

        for location in purpleLocations:
            if containsDupe(location, rune_crafting_locations, 100) == False:
                click_x = left_corner[0] + location[0]
                click_y = left_corner[1] + location[1]
                final_img = cv2.rectangle(final_img, (click_x, click_y), (click_x + 20, click_y + 20), (255, 0, 0), 2)
                final_click.append(location)

        cv2.imwrite('test-final-select-targets.jpg', final_img) 
  
            
    #refill_pos = imagesearch("./images/auto battle/refill_shop.png")
    #print(str(refill_pos))
    #findText()
    


except KeyboardInterrupt:	
    print("Keyboard Interrupt")


