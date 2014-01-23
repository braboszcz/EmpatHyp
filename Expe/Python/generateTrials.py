'''
Generate trial list for Empathyp experiment: go/nogo on right or left hand with rare foot picture for oddball

'''

import random
import os
import csv
import numpy

GO = 1
NOGO = 2
ODDBALL = 3
PAUSE = 4
NULL = 5

#MAXGOINROW = 2

def lefthand(stim):
	return True if stim[0] in  ['L'] else False

def righthand(stim):
	return True if stim[0] in  ['R'] else False

is_go = lefthand

def genTrialList():
	""" 
	generate trial list
	if expe = fmri use fmri jittered ISI list else jitter between 1 and 2 sec	

	"""
	
	writeTrials = csv.writer(open('mytrialList.csv','wb'), delimiter = ',', quotechar = '"')
	header = ['Stim', 'Condition', 'ITI']
	writeTrials.writerow(header)
	
	#------------------------------------------------------------------------
	# define numbers of each type of trials
	#------------------------------------------------------------------------
	nNoGo = 30*2
	nGo = 12 #(  20% de nNoGo. allows for 8 pictures of each conditions)
	nOdd = 5	

	#------------------------------------------------------------------------
	# read stim file name in folder
	#------------------------------------------------------------------------
	for root, dirs, files in os.walk('Stimuli'):
		stimList = files
	random.shuffle(stimList)
	
	#------------------------------------------------------------------------
	# categorize stim into go and no go list
	#------------------------------------------------------------------------
	goStim = [stim for stim in stimList if is_go(stim)]
	nogoStim = [stim for stim in stimList if not is_go(stim)]
	random.shuffle(goStim)
	random.shuffle(nogoStim)	
	#------------------------------------------------------------------------
	# read jitter list
	#------------------------------------------------------------------------
	with open('fMRI_jitter.txt') as jitter:
		ISI = jitter.read().splitlines()	
	#------------------------------------------------------------------------
	# create list of desired amount of Go and No Go Trials and Thought Probes
	#------------------------------------------------------------------------
	# first, mix GO and NOGO when unrelated to PROBES
	
	trials = [NOGO] * nNoGo
	trials += [GO] * nGo
	trials += [ODDBALL] * nOdd
	#trials += [NULL]*nNull
	random.shuffle(trials)
	
	# insert regular null event for resting control condition
	for i in range (1, len(trials)+len(trials)/6,6):
		trials.insert(i, NULL)	
		print i	

	# then insert PAUSE (hypnosis reinforcement) 
	for i in range(1,len(trials), len(trials)/2):
		if i != 1:
			trials.insert(i,PAUSE) 
	#------------------------------------------------------------------------
  	# create list of trials
	#------------------------------------------------------------------------
	
	indnoGo = 0
	indGo = 0
	indOdd = 0
	indNull = 0
	trial = [] 
	
	for i in range(len(trials)):
		if trials[i] == 3:
			trial = ['foot.bmp' ,'oddball', str(ISI[i])]
		
		elif trials[i] == 5:
			trial = ['blank', 'blank', 5]

		elif trials[i] == 4:
			trial = ['pause', 'pause']

		elif trials[i] == 2: 	
			stim = nogoStim[indnoGo]
			trial = [stim,'no-go',str(ISI[i])]
			indnoGo += 1
		#	print indnoGo
		elif trials[i] == 1:	
			stim = goStim[indGo]
			
			trial = [stim,'go',str(ISI[i])]
			indGo += 1
		#	print indGo
		writeTrials.writerow(trial)
	



#genTrialList(305, 1)
genTrialList()	
