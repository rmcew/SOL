#Mind in the Eyes task for the AT Adults study

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
import numpy as np
import pandas as pd
import sys, os, re

#Directory:
cwd = os.path.dirname(__file__)

#GUI:
expName = "Mind_in_the_Eyes Adults"
expInfo = {"Subject ID":""}
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName)
if dlg.OK == False:
    core.quit()
if expInfo["Subject ID"] == "":
    raise ValueError("Please input the subject's ID")
   
#Window:
win = visual.Window(fullscr = True, pos = (0,0), units = 'norm', color = 'White')


#********************************
# REMOVED, WE WANT TO USE MOUSE *
#********************************
#Turn Mouse Off:
#event.Mouse(visible=False)

#Timers:
timer = core.Clock() #Basic timer
trialTimer = core.Clock() #Records time of a single trial, but does so in a cumulative manner 

#Load stim file, make a few additions, and randomize:
stim_df = pd.read_csv('Stimuli.csv')
stim_df['Stimulus'] = np.nan #Creat new column for pathway to esch picture
for i in range(len(stim_df)):
    stim_df['Stimulus'][i] = os.path.join(cwd + "/Pictures/%s.png" % i) #Input picture pathway to each row
stim_df = pd.concat([stim_df[:1], stim_df[1:].sample(len(stim_df[1:]))]).reset_index(drop=True) #Randomize the order of the trial rows, but always have the practice run come first
stim_df.drop('Index', axis=1, inplace=True) #Remove redundant index row

#The next 6 lines randomize the text stimuli so that they will be placed on screen at different locations for each new exp run. 
vals = stim_df.values
cols12 = stim_df.ix[:,0]
lastcols = stim_df.ix[:,len(stim_df.columns)-2:len(stim_df.columns)]
middle = pd.DataFrame([np.random.permutation(i) for i in vals[:,1:5]])
middle.columns = ['Resp1','Resp2','Resp3','Resp4']
stim_df = pd.concat([cols12, middle, lastcols], axis=1)

'''#Checking for output (data) file:
fileLocation = os.path.join(cwd + "/Data/%s" % expInfo["Subject ID"])
if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)
os.chdir(fileLocation)
if os.path.isfile("logFile.csv"):
    raise ValueError ("A log and stat file already exist for this participant")
'''

#List and Panda File Header:
run_param_list = []
header = ['Trial','TrialStart','Stimulus','StimGender','Accuracy','RT','Response','CorrectResponse','Responses','TrialEnd']

#Define text/visual stimuli and location 
text = visual.TextStim(win, text = '', pos = (0,0), height = 0.06, color='Black', wrapWidth = 1.3) 
image = visual.ImageStim(win = win, pos = (0,0), size = (1.1,0.75), image = stim_df["Stimulus"][0])
coordinates = [(-0.4,0.6),(0.4,0.6),(-0.4,-0.6),(0.4,-0.6)]

#Instruction Page:
text.text = 'For each set of eyes, indicate which word best describes what the person in the picture is thinking or feeling.\n\n\n1=Top Left     ||     2=Top Right     ||     3=Bottom Left     ||     4=Bottom Right\n\n\nYou may feel that more than one word is applicable but please choose just one word, the word which you consider to be most suitable. Before making your choice, make sure that you have read all 4 words. You should try to do the task as quickly as possible but you will not be timed.\n\nPlease read and make sure you know all of the words and definitions in the handout.\n\nPress any key to begin' 
text.draw()
win.flip()
while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if len(theseKeys):
        break

#Begin Trials:
i = 0
while i < len(stim_df):
    trial_start = trialTimer.getTime()
    timer.reset()
    event_output = []
    stim_new = np.array([stim_df["Resp%s" % x][i] for x in range(1,5)])
    
    #Fixation before stimulus presentation: 
    text.text = "+"
    text.pos = (0,0)
    text.draw()
    win.flip()
    t0 = timer.getTime()
    while timer.getTime() < 0.5 + t0:
        if "escape" in theseKeys:
            core.quit()
    
    for j in range(4):
        #Load text stim:
        text.text = str(j+1) + "- " + stim_new[j]
        text.pos = coordinates[j]
        text.draw()
        #Load pic stim:
        image.image = stim_df["Stimulus"][i]
        image.draw()
    win.flip()
    stim_onset = timer.getTime()
    
    event_press = event.clearEvents(eventType = "keyboard")
    RT = "N/A"
    response = None
    while True:
        event_press = event.getKeys(keyList = ["1","2","3","4"])
        if event_press:
            RT = timer.getTime() - stim_onset
            response = event_press[-1]
            if stim_df['Resp%s' %response][i] == stim_df['CorrAnswer'][i]:
                acc = 1
            else:
                acc = 0
            break
            
        if event.getKeys(keyList = ["escape"]):
            core.quit()
                  
    if i == 0:
        trialType = 'practice'
        if stim_df['Resp%s' %response][i] == stim_df['CorrAnswer'][i]:
            text.text = "That was correct. You will now begin the actual trials.\n\n\tThe first trial will start as soon as you are ready.\n\n\t\tPress the SPACEBAR to continue"
            text.pos = (0,0)
            text.draw()
            win.flip()
            while True:            
                theseKeys = event.getKeys(keyList = ["space"])
                if "escape" in theseKeys:
                    core.quit()
                if len(theseKeys):
                    break
            i += 1     

        else:
            text.text = "That was incorrect.\n\nPlease try again.\n\nPress the SPACEBAR to continue"
            text.pos = (0,0)
            text.draw()
            win.flip()
            while True:
                theseKeys = event.getKeys(keyList = ["space"])
                if "escape" in theseKeys:
                    core.quit()
                if len(theseKeys):
                    break
    else:
        text.text = "Press the SPACEBAR to continue"
        text.pos = (3,0)
        text.draw()
        win.flip()
        while True:
            theseKeys = event.getKeys(keyList = ["space"])
            if "escape" in theseKeys:
                core.quit()
            if len(theseKeys):
                break
        #List of the text stimuli for each trial:
        text_stim = []
        for k in range(1,5):
            text_stim.append(stim_df['Resp%s' % k][i])
            
        trial_end = trialTimer.getTime()
                
        #Panda Output File
        run_param_list.append([i,round(trial_start,4), str(''.join(re.findall('\d+', stim_df['Stimulus'][i]))) + ".png", 
        stim_df["Gender"][i], acc, round(RT, 4), stim_df['Resp%s' %response][i], stim_df['CorrAnswer'][i], text_stim, round(trial_end,4)])
        
        fid = pd.DataFrame(run_param_list, columns = header)
        fid.to_csv("logFile.csv", header = True)
        
        i += 1
        
#Create Stat Sheet for Experimental Session:       
nIncorrect = fid["Accuracy"].value_counts()[0]
nCorrect = fid["Accuracy"].value_counts()[1]
nTrials = len(fid)
ExpDuration = round((fid["TrialEnd"].ix[-1:][len(fid)-1]),4)
TotalAcc = round((nCorrect/nTrials),4)

run_param_list2 = []
header = ['Incorrect','Correct','NumTrials','Experiment Duration','Total Accuracy']
run_param_list2.append([nIncorrect, nCorrect, nTrials, ExpDuration, TotalAcc])

fid2 = pd.DataFrame(run_param_list2, columns = header)
fid2.to_csv("StatFile.csv", header = True)

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