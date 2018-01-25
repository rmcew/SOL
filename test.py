'''
Title  : Pandas Row Shuffler 
Author : Felan Carlo Garcia
'''
import numpy as np
import os
import pandas as pd




def main(outputfilename):
  stim_df = pd.read_excel('SOLItemList_2017-11-16.xlsx')
  newdf = stim_df[['ItemNumber', 'TriviaQuestion']]
  
  
