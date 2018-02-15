from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
import numpy as np
import pandas as pd
import sys, os, re
import time
import random



stim_df = pd.read_excel('SOLItemList_2017-11-16.xlsx')
stim_monetaryCombination = pd.read_excel('SOLMonetaryMatches_2017-11-16.xlsx')
stim_trivia = stim_df[['ItemNumber','TriviaFact', 'TriviaQuestion']]
stim_learn = stim_df[['ItemNumber','LearnFact', 'LearnQuestion']]
stim_shareQuestion = stim_df[['ItemNumber','ShareQuestion']]


print stim_shareQuestion
stim_shareQuestion.drop(1, inplace = True)
print stim_shareQuestion