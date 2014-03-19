# -*- coding: utf8 -*-
#!/usr/bin/env python


'''
Script for a thermic pain localizer

'''

import time
import sys
from psychopy import visual,event,core, data, logging, gui
import csv
import random
import os
from psychopy.hardware.emulator import launchScan
from psychopy import parallel
import numpy as np
#import msa


# create timer
globalClock = core.Clock()

#----------------------------
#   store expe info
#----------------------------
expName = 'PainLoc-Empathyp'  
expInfo = {'participant':'', 'session': '', 'threshold':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel  

expInfo['date'] = data.getDateStr()  # add a simple timestamp  
expInfo['expName'] = expName

# Experiment handler
thisExp = data.ExperimentHandler(name=expName, version='',
	    extraInfo=expInfo, runtimeInfo=None,
	    originPath=None,
	    savePickle=False, saveWideText=False) #prevent the experiment handler to write expe data upon termination (and overwriting our files)
	

# Setup files for logfile  saving

if not os.path.isdir('Logdata'):
    os.makedirs('Logdata')  # if this fails (e.g. permissions) we will get error
    filename = 'Logdata' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['session'])
    logging.setDefaultClock(globalClock)
    logFileExp = logging.LogFile(filename +'.log', level=logging.EXP)
    logging.console.setLevel(logging.INFO)  # this outputs to the screen, not a file

save_filename= '%s_%s' %(expInfo['participant'], expInfo['session'])
trials = data.TrialHandler([], nReps=1, method='sequential', extraInfo=expInfo)
trials.data.addDataType('stim type')
trials.data.addDataType('stim onset')
trials.data.addDataType('base onset')
trials.data.addDataType('ISI')
   

#----------------------
# Thermode settings
#---------------------
# init thermode
#Msa_init = '365_Thermod_v5_fmri_v.6_748_130827.ini'
#msa.MsaOpen(1,Msa_init) # change for 4

# thermode variables
stim_duration = 2
slope = 3
base_temp = 36
no_nox_temp = 40
nox_temp = expInfo['threshold']

#-------------------------
# Pain localizer settings
#-------------------------

n_stim = 6
nox = 1
no_nox = 2

stim_list = [nox] * n_stim 
stim_list += [no_nox] *n_stim

random.shuffle(stim_list)

isi_list = np.random.uniform(8,18, 12)




#---------------------------------------
# Setup the Window
#---------------------------------------
win = visual.Window([1280,1024],color = [0.5, 0.5, 0.5],monitor ='testMonitor',  units='height', fullscr = False, colorSpace = 'rgb')

change_temp =  visual.TextStim(win=win, ori=0, name='change_temp',
text="la temperature change", font='Arial', pos=[0, 0], height=0.04, wrapWidth=None,color='black', colorSpace='rgb', opacity=1, depth=0.0)


the_end = visual.TextStim(win=win, ori=0, name='theEnd',
text="Fin", font='Arial', pos=[0, 0], height=0.04, wrapWidth=None,color='black', colorSpace='rgb', opacity=1, depth=0.0)

fixation_cross=visual.TextStim(win=win, ori=0, name='fixation_cross', text='+', font='Arial',pos=[0, 0], height=0.06,color='black')
fixation_cross.setLineWidth = 0.4

# ---------------------------------
#!!!!!!! insert fmri launchscan
#-----------------------------------

for stim in range(len(stim_list)):
# save data for the trial loop using psychopy function
    trials.saveAsWideText(save_filename + '.csv', delim=',', appendFile = False)
    #trials.addData('scanOnset', onset)
    thisResp = [] # to store resp key and resp time
    stim_onset = globalClock.getTime()
    


    if stim_list[stim] == 1:
        print nox_temp
        #msa.MsaReachStimTemp(nox_temp, slope)
        
        while globalClock.getTime() < stim_onset + stim_duration:   
            change_temp.draw(win)
            win.flip()
       # core.wait(stim_duration)
    else:
        print no_nox_temp
        #msa.MsaReachStimTemp(no_nox_temp, slope)
        core.wait(stim_duration)
    
    fixation_cross.draw(win)
    win.flip()
    print base_temp
    base_onset = globalClock.getTime()
    #msa.MsaReachStimTemp(base_temp, slope)
    core.wait(round(isi_list[stim], 2))
    
    trials.addData('stim type', stim_list[stim])
    trials.addData('stim onset', stim_onset)
    trials.addData('base onset', base_onset)
    trials.addData('ISI', isi_list[stim])

#msa.MsaClose()
the_end.draw()
win.flip()
core.wait(3)

