#Kate Project

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
import numpy as np
import pandas as pd
import sys, os, re
import time
import random

#Directory:
cwd = os.path.dirname(__file__)


#**********************************************
#  Need to change this information            *
#**********************************************
#GUI:
expName = "SOL"
expInfo = {"Subject ID":"","Sex": ""}
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName, order = ["Subject ID", "Sex"])
if dlg.OK == False:
    core.quit()
if expInfo["Subject ID"] == "":
    raise ValueError("Please input the subject's ID")

#Window:
win = visual.Window(fullscr = True, pos = (0,0), units = 'norm', color = 'White')



#Timers:
timer = core.Clock() #Basic timer
trialTimer = core.Clock() #Records time of a single trial, but does so in a cumulative manner 

#Load stim file, make a few additions, and randomize:
stim_df = pd.read_excel('SOLItemList_2017-11-16.xlsx')
stim_monetaryCombination = pd.read_excel('SOLMonetaryMatches_2017-11-16.xlsx')
stim_trivia = stim_df[['ItemNumber','TriviaFact', 'TriviaQuestion']]
stim_learn = stim_df[['ItemNumber','LearnFact', 'LearnQuestion']]
stim_shareQuestion = stim_df[['ItemNumber','ShareQuestion']]


'''
for i in range(len(stim_df)):
    stim_df['Stimulus'][i] = os.path.join(cwd + "/Pictures/%s.png" % i) #Input picture pathway to each row
'''
stim_monetaryCombination = stim_monetaryCombination.sample(frac=1).reset_index(drop=True)
stim_df = stim_df.sample(frac=1).reset_index(drop=True) #Randomize the order of the trial rows, but always have the practice run come first
stim_trivia = stim_trivia.sample(frac=1).reset_index(drop=True)
stim_learn = stim_learn.sample(frac=1).reset_index(drop=True)
stim_shareQuestion = stim_shareQuestion.sample(frac=1).reset_index(drop=True)


#stim_df.drop('ItemNumber', axis=1, inplace=True) #Remove redundant ItemNumber column


#Define text/visual stimuli and location 
# Static Variables
moneyScreenPrompt = visual.TextStim(win, text = 'Make a Choice:', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
headerText = visual.TextStim(win, pos = (0,.5), height = 0.13, color='Black', wrapWidth = 1.3) 
triviaText = visual.TextStim(win, pos = (0,-.3), height = 0.07, color='Black', wrapWidth = 1.3) 
leftChoiceText = visual.TextStim(win, pos = (-.5, -.05), height = 0.05, color='Black', wrapWidth = 1.3) 
leftBubbleText = visual.TextStim(win, pos = (-.51, 0), height = 0.05, color='Black', wrapWidth = .44) 
rightBubbleText = visual.TextStim(win, pos = (.51, 0), height = 0.05, color='Black', wrapWidth = .44) 
rightChoiceText = visual.TextStim(win, pos = (.5,-.05), height = 0.05, color='Black', wrapWidth = 1.3)
leftValueText = visual.TextStim(win, pos = (-.5, -.11), height = 0.05, color='Black', wrapWidth = 1.3) 
rightValueText = visual.TextStim(win, pos = (.5,-.11), height = 0.05, color='Black', wrapWidth = 1.3)
topLeftText = visual.TextStim(win, pos = (-.5, .25), height = 0.05, color='Black', wrapWidth = 1.3, text = "1 = Select UT") 
topRightText = visual.TextStim(win, pos = (.5,.25), height = 0.05, color='Black', wrapWidth = 1.3, text = "2 = Select UTSA")
bottomLeftText = visual.TextStim(win, pos = (-.5, -.25), height = 0.05, color='Black', wrapWidth = 1.3, text = "3 = Select UNT") 
bottomRightText = visual.TextStim(win, pos = (.5,-.25), height = 0.05, color='Black', wrapWidth = 1.3, text = "4 = Select Texas A&M")
#partnerName = visual.TextStim(win, text = 'Make a Choice', pos = (0,.4), height = 0.06, color='Black', wrapWidth = 1.3, bold='True') 
shareScreenPrompt = visual.TextStim(win, pos = (0,.55), height = 0.13, color='Black', wrapWidth = 1.5, alignHoriz='center') 
sendingMessage = visual.TextStim(win, text = 'Sending message...', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
partnerReading = visual.TextStim(win, pos = (0,0), height = 0.13, color='Black', wrapWidth = 1.3) 
messageRead = visual.TextStim(win, text = 'Message read', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
learnScreenPrompt = visual.TextStim(win, pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.5, alignHoriz='center') 
waitingToLearn = visual.TextStim(win, text = 'Waiting for message', pos = (0,0), height = 0.13, color='Black', wrapWidth = 1.3) 
messageReceived = visual.TextStim(win, pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
triviaScreenPrompt = visual.TextStim(win, text = 'WHAT DO YOU WANT TO KNOW ABOUT?', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
computerWaiting = visual.TextStim(win, text = 'COMPUTER FINDING FACT IN DATABASE...', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
computerMessageReceived = visual.TextStim(win, text = 'Press any key to confirm information read', pos = (0,-.4), height = 0.13, color='Black', wrapWidth = 1.3) 
computerConfirmation = visual.TextStim(win, text = 'Information read', pos = (0,.4), height = 0.13, color='Black', wrapWidth = 1.3) 
connecting = visual.TextStim(win, pos = (0,.4), height = 0.13, color = 'Black', wrapWidth = 1.3)
connectionLost = visual.TextStim(win, text = 'Connection to UT campus lost/n/nReconnecting...', pos = (0,.4), height = 0.13, color = 'Black', wrapWidth = 1.3)
connectedTo = visual.TextStim(win, pos = (0,.5), height = 0.13, color = 'Black', wrapWidth = 1.3)
connectingToPartner = visual.TextStim(win, pos = (0,.5), height = 0.13, color = 'Black', wrapWidth = 1.3)
eligiblePartners = visual.TextStim(win, text = 'Eligible Chat Partners:\n                2', pos = (0,.1), height = 0.13, color = 'Black')
displayPartners = visual.TextStim(win, text = 'Display Chat Partners?\n      Yes            No', pos = (0,-.3), height = 0.13, color = 'Black')
selectPartnerText = visual.TextStim(win, text = 'Please select your chat partner', pos = (0,.7), height = 0.13, color = 'Black', wrapWidth = 1.3)
leftPartnerText = visual.TextStim(win, pos = (-.4, .3), height = 0.07, color = "Black", wrapWidth = 1.3)
rightPartnerText = visual.TextStim(win, pos = (.4, .3), height = 0.07, color = "Black", wrapWidth = 1.3)

if str.lower(str(expInfo["Sex"])) == "m" or str.lower(str(expInfo["Sex"])) == "male":
    partnerList = pd.read_csv('PartnerNamesMale.csv')
    sex = "male"
elif str.lower(str(expInfo["Sex"])) == "f" or str.lower(str(expInfo["Sex"])) == "female":
    partnerList = pd.read_csv('PartnerNamesFemale.csv')
    sex = "female"
else:
    raise ValueError("Please enter M or F in the sex field") #Throw error if invalid input
    
#Randomize partner list
partnerList = partnerList.sample(frac=1).reset_index(drop=True) 

global WhichSelected
global RT
global LeftDisplay
global RightDisplay
global WhichSelected2
global RT2
global HowLongLearnDelay
global HowLongToPressReceipt
global WhatLearnedFactWas



# Variables
text = visual.TextStim(win, text = '', pos = (0,0), height = 0.06, color='Black', wrapWidth = 1.3) 
coordinates = [(-0.4,0.6),(0.4,0.6),(-0.5,-0.2),(0.5,-0.2)]


# Images
blueBubbleLeft = visual.ImageStim(win = win, pos = (-.52,0), image = cwd + "\Pictures\chat-blue.png")
blueBubbleRight = visual.ImageStim(win = win, pos = (.52,0), image = cwd + "\Pictures\chat-blue.png")
greenBubbleLeft = visual.ImageStim(win = win, pos = (-.52,-.3), image = cwd + "\Pictures\chat-green.png")
greenBubbleRight = visual.ImageStim(win = win, pos = (.52,0), image = cwd + "\Pictures\chat-green.png")
loadGif = visual.ImageStim(win = win, pos = (0,0), image = cwd + "\loading.gif")
leftPartnerImg = visual.ImageStim(win = win, pos = (-.4,0))
rightPartnerImg= visual.ImageStim(win = win, pos = (.4,0))
checkmarkIcon = visual.ImageStim(win = win, pos = (-.52, -.3), image = cwd + "\Pictures\CheckmarkIcon.png", size = .2)
intro = visual.ImageStim(win = win, pos = (0,0), size = 2, image = cwd + "\Pictures\Intro.png")

#*********************************************************************
#   This creates output file, input correct column names here        *
#*********************************************************************

#Checking for output (data) file:
owd = os.getcwd()
fileLocation = os.path.join(cwd + "/Data/%s" % expInfo["Subject ID"])
if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)
os.chdir(fileLocation)

#Checks to see if this participant ID has been used before. Comment out while testing
if os.path.isfile("logFile.csv"):
    raise ValueError ("A log and stat file already exist for this participant")

os.chdir(owd)

#List and Panda File Header:
run_param_list = []
header = ['TrialNumber','LeftAmount','RightAmount','LeftOption','RightOption','WhichSelected','RT','LeftDisplay','RightDisplay','WhichSelected', 'RT2', 'HowLongLearnDelay', 'HowLongToPressReceipt', 'WhatLearnedFactWas']




#*********************************************************
#                       Functions                        *
#*********************************************************

#Select Campus
def SelectCampus():
    headerText.text = "Select University Chat Site"
    headerText.draw()
    topLeftText.draw()
    topRightText.draw()
    bottomLeftText.draw()
    bottomRightText.draw()
    win.flip()
    key_press = event.waitKeys(keyList = ["escape","1", "2", "3", "4"])
    headerText.pos = (0,0)
    if "escape" in key_press:
        core.quit()
    if "1" in key_press:
        location = "UT lab"
    if "2" in key_press:
        location = "UTSA lab"
    if "3" in key_press:
        location = "UNT lab"
    if "4" in key_press:
        location = "Texas A&M lab"
    
    return location


#   Connecting Gif   #
def Connecting(headerString, numberOfLoops):
    timer = 0
    while timer < numberOfLoops:
        imgNum = 1
        while imgNum< 13:
            time.sleep(.08)
            headerString.draw()
            loadGif.image = cwd + '\Pictures\loading\\' + str(imgNum) + '.gif'
            loadGif.draw()
            win.flip()
            imgNum = imgNum + 1
        timer = timer+1

#   Monetary Options Screen   #
def MonetaryScreen(questionNumber):
    global RT
    timer_start = time.time()
    win.setColor((255, 255, 255), 'rgb255')
    win.flip()
    moneyRow = stim_monetaryCombination['ItemNumber'][questionNumber]
    leftChoice = stim_monetaryCombination['LeftCategory'][questionNumber]
    rightChoice = stim_monetaryCombination['RightCategory'][questionNumber]
    leftValue = stim_monetaryCombination['LeftAmount'][questionNumber]
    rightValue = stim_monetaryCombination['RightAmount'][questionNumber]
    
    leftChoiceText.text = leftChoice
    rightChoiceText.text = rightChoice
    leftValueText.text = str(leftValue) + ' cents'
    rightValueText.text = str(rightValue) + ' cents'
    
    moneyScreenPrompt.draw()
    leftChoiceText.draw()
    rightChoiceText.draw()
    leftValueText.draw()
    rightValueText.draw()
    
    win.flip()
    
    #moneyScreenPrompt.draw()
    #win.flip()
    #while True:
    key_press = event.waitKeys(keyList = ["escape","z","m"])
    timer_stop = time.time()
    RT = timer_stop-timer_start
    
    if "escape" in key_press:
        core.quit()

    if "z" in key_press:
        #Display only the selected choice for 1 second
        leftChoiceText.draw()
        win.flip()
        time.sleep(1)
        
        MonetaryScreen.selected = leftChoice
        Choice(leftChoice, questionNumber)
    if "m" in key_press:
        #Display only the selected choice for 1 second
        rightChoiceText.draw()
        win.flip()
        time.sleep(1)
        
        MonetaryScreen.selected = rightChoice
        Choice(rightChoice, questionNumber)
    

def Choice(choice, questionNumber):
    global WhichSelected
    if choice == "Share":
        WhichSelected = "Share"
        Share(questionNumber)
    if choice == "Learn":
        WhichSelected = "Learn"
        Learn(questionNumber)
    if choice == "Trivia":
        WhichSelected = "Trivia"
        Trivia(questionNumber)

#   Partner Selection   # Remember to put a sex bool as parameter
def PartnerSelection(sex):    
    leftPartnerImg.image = partnerList['PictureFileName'][1]
    rightPartnerImg.image = partnerList['PictureFileName'][2]
    leftPartnerText.text = str(partnerList['PersonName'][1]) + ' (' + str(partnerList['PersonAge'][1]) + ')'
    rightPartnerText.text = str(partnerList['PersonName'][2]) + ' (' + str(partnerList['PersonAge'][2]) + ')'
    rightPartnerAge = partnerList['PersonAge'][2]
    selectPartnerText.draw()
    leftPartnerImg.draw()
    rightPartnerImg.draw()
    leftPartnerText.draw()
    rightPartnerText.draw()
    win.flip()
    while True:
        theseKeys = event.waitKeys(keyList = ['escape', 'z', 'm'])
        if "escape" in theseKeys:
            core.quit()
        if 'z' in theseKeys:
            partnerName = str(partnerList['PersonName'][1])
        if 'm' in theseKeys:
            partnerName = str(partnerList['PersonName'][2])
        if len(theseKeys):
            break
    #Set partner name for "connecting to" screen
    connectingToPartner.text = 'Connecting to ' + partnerName +'...'
    partnerReading.text = partnerName + ' is reading...'
    learnScreenPrompt.text = partnerName + ' asks: What do you want to learn about me?'
    shareScreenPrompt.text = 'What do you want to tell ' + partnerName + ' about yourself?'
    messageReceived.text = 'Press SPACEBAR to let ' + partnerName + ' know that you received the message'
    

#   Share Category   #
def Share(questionNumber):
    global RT2
    global LeftDisplay
    global RightDisplay
    global WhichSelected2
    global HowLongLearnDelay
    global HowLongToPressReceipt
    global WhatLearnedFactWas
    WhatLearnedFactWas = "N/A"
    HowLongToPressReceipt = "N/A"
    
    timer_start = time.time()
    #Put text back in the right place
    leftBubbleText.pos = (-.52, 0)

    
    win.setColor((218, 227, 245), 'rgb255')
    win.flip()
    shareScreenPrompt.draw()
    win.flip()
    time.sleep(.250)
    shareScreenPrompt.draw()
    blueBubbleLeft.draw()
    leftBubbleText.text = stim_shareQuestion['ShareQuestion'][questionNumber]        #replace index
    Share.leftChoice = leftBubbleText.text
    LeftDisplay = Share.leftChoice
    leftBubbleText.draw()
    blueBubbleRight.draw()
    rightBubbleText.text = stim_shareQuestion['ShareQuestion'][questionNumber+1]        #replace index
    Share.rightChoice = rightBubbleText.text
    RightDisplay = Share.rightChoice
    rightBubbleText.draw()
    win.flip()
    
    
    key_press = event.waitKeys(keyList = ["escape","z","m"])
    timer_stop = time.time()
    RT2 = timer_stop-timer_start
    
    if "escape" in key_press:
        core.quit()
    if "z" in key_press:
        Share.selected = "Left"
        WhichSelected2 = Share.leftChoice
        sendingMessage.draw()
        blueBubbleRight.draw()
        rightBubbleText.text = stim_shareQuestion['ShareQuestion'][questionNumber]        #replace index
        rightBubbleText.draw()
        leftBubbleText.text = "..."
        leftBubbleText.pos = (-.52, -.3)
        greenBubbleLeft.pos = (-.52,-.3)
        greenBubbleLeft.draw()
        leftBubbleText.draw()
        win.flip()
        HowLongLearnDelay = random.uniform(1.5,3)
        time.sleep(HowLongLearnDelay)
        
    if "m" in key_press:
        Share.selected = "Right"
        WhichSelected2 = Share.rightChoice
        sendingMessage.draw()
        blueBubbleRight.draw()
        rightBubbleText.text = stim_shareQuestion['ShareQuestion'][questionNumber+1]        #replace index
        rightBubbleText.draw()
        leftBubbleText.text = "..."
        leftBubbleText.pos = (-.52, -.3)
        greenBubbleLeft.pos = (-.52,-.3)
        greenBubbleLeft.draw()
        leftBubbleText.draw()
        win.flip()
        HowLongLearnDelay = random.uniform(1.5,3)
        time.sleep(HowLongLearnDelay)

    messageRead.draw()
    greenBubbleLeft.draw()
    blueBubbleRight.draw()
    rightBubbleText.draw()
    checkmarkIcon.pos = (-.52, -.3)
    checkmarkIcon.draw()
    win.flip()
    time.sleep(1.2)



#   Learn Category   #
def Learn(questionNumber):
    global RT2
    global LeftDisplay
    global RightDisplay
    global WhichSelected2
    global HowLongLearnDelay
    global HowLongToPressReceipt
    global WhatLearnedFactWas
    HowLongLearnDelay = "N/A"
    
    leftBubbleText.pos = (-.52, 0)
    timer_start = time.time()
    win.setColor((255, 230, 153), 'rgb255')
    win.flip()
    win.flip()
    
    learnScreenPrompt.draw()
    win.flip()
    time.sleep(.250)
    learnScreenPrompt.draw()
    blueBubbleLeft.draw()
    leftBubbleText.text = stim_learn['LearnQuestion'][questionNumber]        #replace index
    Learn.leftChoice = leftBubbleText.text
    LeftDisplay = Learn.leftChoice
    leftBubbleText.draw()
    blueBubbleRight.draw()
    rightBubbleText.text = stim_learn['LearnQuestion'][questionNumber+1]        #replace index
    Learn.rightChoice = rightBubbleText.text
    RightDisplay = Learn.rightChoice
    rightBubbleText.draw()
    win.flip()
    
    
    key_press = event.waitKeys(keyList = ["escape","z","m"])
    timer_stop = time.time()
    RT2 = timer_stop-timer_start
    
    if "escape" in key_press:
        core.quit()
    if "z" in key_press:
        Learn.selected = "Left"
        WhichSelected2 = Learn.leftChoice
        sendingMessage.draw()
        blueBubbleRight.draw()
        rightBubbleText.text = stim_learn['LearnQuestion'][questionNumber]        #replace index
        rightBubbleText.draw()
        win.flip()
        time.sleep(1.5)
        greenBubbleLeft.draw()
        leftBubbleText.text = stim_learn['LearnFact'][questionNumber]
        leftBubbleText.pos = (-.52, -.3)
        leftBubbleText.draw()
        blueBubbleRight.draw()
        rightBubbleText.draw()
        messageReceived.draw()
        win.flip()
        timer_start = time.time()
        event.waitKeys(keyList = ["space"])
        timer_stop = time.time()
        HowLongToPressReceipt = timer_stop - timer_start
        WhatLearnedFactWas = stim_learn['LearnFact'][questionNumber]
        
        
    if "m" in key_press:
        Learn.selected = "Right"
        WhichSelected2 = Learn.rightChoice
        sendingMessage.draw()
        blueBubbleRight.draw()
        rightBubbleText.text = stim_learn['LearnQuestion'][questionNumber+1]        #replace index
        rightBubbleText.draw()
        win.flip()
        time.sleep(1.5)
        greenBubbleLeft.draw()
        blueBubbleRight.draw()
        rightBubbleText.draw()
        leftBubbleText.text = stim_learn['LearnFact'][questionNumber+1]
        leftBubbleText.pos = (-.52, -.3)
        leftBubbleText.draw()
        messageReceived.draw()
        win.flip()
        timer_start = time.time()
        event.waitKeys(keyList = ["space"])
        timer_stop = time.time()
        HowLongToPressReceipt = timer_stop - timer_start
        WhatLearnedFactWas = stim_learn['LearnFact'][questionNumber+1]
    
    
    greenBubbleLeft.draw()
    blueBubbleRight.pos = (.52, -.6) #Temporarily move blue bubble down
    blueBubbleRight.draw()
    leftBubbleText.draw()
    checkmarkIcon.pos = (.52, -.6)
    checkmarkIcon.draw()
    
    win.flip()
    blueBubbleRight.pos = (.52, 0) #Put blue bubble back in correct place
    time.sleep(1.5)
    

#   Trivia Category  #
def Trivia(questionNumber):
    global RT2
    global LeftDisplay
    global RightDisplay
    global WhichSelected2
    global HowLongLearnDelay
    global HowLongToPressReceipt
    global WhatLearnedFactWas
    HowLongLearnDelay = "N/A"
    leftBubbleText.pos = (-.52, 0)
    timer_start = time.time()
    
    if stim_trivia['TriviaQuestion'][questionNumber] == stim_trivia['TriviaQuestion'][questionNumber+1]:
        Connecting(connectionLost, 2)
    else:
        win.setColor((248, 203, 173), 'rgb255')
        
        win.flip()
        win.flip()
        
        triviaScreenPrompt.draw()
        win.flip()
        time.sleep(.250)
        triviaScreenPrompt.draw()

        leftBubbleText.text = stim_trivia['TriviaQuestion'][questionNumber]        #replace index
        Trivia.leftChoice = leftBubbleText.text
        LeftDisplay = Trivia.leftChoice
        leftBubbleText.draw()
        rightBubbleText.text = stim_trivia['TriviaQuestion'][questionNumber+1]        #replace index
        Trivia.rightChoice = rightBubbleText.text
        RightDisplay = Trivia.rightChoice
        rightBubbleText.draw()
        win.flip()
        
        
        key_press = event.waitKeys(keyList = ["escape","z","m"])
        timer_stop = time.time()
        RT2 = timer_stop-timer_start
        
        if "escape" in key_press:
            core.quit()
            
        if "z" in key_press:
            Trivia.selected = "Left"
            WhichSelected2 = Trivia.leftChoice
            computerWaiting.draw()
            win.flip()
            time.sleep(.5)
            triviaText.text = stim_trivia['TriviaFact'][questionNumber]        #replace index
            triviaText.draw()
            headerText.pos = (0, .4)
            headerText.text = "Press any key to verify message read"
            headerText.draw()
            win.flip()
            timer_start = time.time()
            event.waitKeys(keyList = ["space"])
            timer_stop = time.time()
            HowLongToPressReceipt = timer_stop - timer_start
            WhatLearnedFactWas = stim_trivia['TriviaFact'][questionNumber]
            
        if "m" in key_press:
            Trivia.selected = "Right"
            WhichSelected2 = Trivia.rightChoice
            computerWaiting.draw()
            win.flip()
            time.sleep(.5)
            triviaText.text = stim_trivia['TriviaFact'][questionNumber+1]        #replace index
            triviaText.draw()
            headerText.pos = (0, .4)
            headerText.text = "Press any key to verify message read"
            headerText.draw()
            win.flip()
            time.sleep(.5)
            timer_start = time.time()
            event.waitKeys(keyList = ["space"])
            timer_stop = time.time()
            HowLongToPressReceipt    = timer_stop - timer_start
            WhatLearnedFactWas = stim_trivia['TriviaFact'][questionNumber+1]
        
        headerText.pos = (0,0)
        headerText.text = "Information Received"
        headerText.draw()
        win.flip()
        time.sleep(1)
        
        


        #event.waitKeys()

#Break function
def Break():    #I would consider changing the background to something unique here
    
    headerText.text = "Great work! Press the spacebar to keep chatting"
    headerText.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])

def StartTrials():
    headerText.text = "Press spacebar to begin chat"
    headerText.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])
    
#*******************************************************
#               START MAIN PROGRAM                     *
#*******************************************************
#Intro Slide
intro.draw()
win.flip()
while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if len(theseKeys):
        break
        
        

#Connected to Page:
lab = SelectCampus()
connecting.text = "Connecting to " + str(lab) + "..."
Connecting(connecting, 3)
connectedTo.text = 'Connected to:\n     ' + str(lab)
connectedTo.draw()
eligiblePartners.draw()
displayPartners.draw()
win.flip()
while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if len(theseKeys):
        break
        
        


PartnerSelection(sex)
Connecting(connectingToPartner, 2)


StartTrials()

#   Begin Trials   #
trialNumber = 1
questionNumber = 1
while (trialNumber < 5): #195
    trial_start = trialTimer.getTime()
    timer.reset()
    event_output = []
    
    if trialNumber == 65 or trialNumber == 130:
        Break()
    
    #Fixation before stimulus presentation: 
    text.text = "+"
    text.pos = (0,0)
    text.draw()
    win.flip()
    t0 = timer.getTime()
    while timer.getTime() < 0.5 + t0:
        if "escape" in theseKeys:
            core.quit()
            
    MonetaryScreen(questionNumber)

    #Panda Output File
    run_param_list.append([trialNumber,stim_monetaryCombination['LeftAmount'][questionNumber],
    stim_monetaryCombination['RightAmount'][questionNumber],stim_monetaryCombination['LeftCategory'][questionNumber],
    stim_monetaryCombination['RightCategory'][questionNumber], WhichSelected,RT,LeftDisplay,RightDisplay,
    WhichSelected2,RT2,HowLongLearnDelay,HowLongToPressReceipt,WhatLearnedFactWas])
    
    print run_param_list
    
    fid = pd.DataFrame(run_param_list, columns = header)
    fid.to_csv(os.path.join(fileLocation, "logFile.csv"), header = True, index = False, encoding = "utf-8")
    
    trialNumber = trialNumber + 1 
    questionNumber = questionNumber + 2



#End of Experiment:
text.text = "Thank you for participating.\n\nPlease contact experimenter."
text.pos = (0,0)
text.draw()
win.flip()
while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if len(theseKeys):
        break

#Close Psychopy:
win.close()
core.quit()