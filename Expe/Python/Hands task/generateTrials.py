'''
Generate trial list for Empathyp experiment: go/nogo on right or left hand with rare foot picture for oddball

'''

import random
import os
import csv
import numpy
import ipdb

GO = 1
NEG= 2
ODDBALL = 3
PAUSE = 4
NULL = 5
NEUT=6

#MAXGOINROW = 2

def lefthand(stim):
	return True if stim[0] in  ['L'] else False

#def righthand(stim):
#	return True if stim[0] in  ['R'] else False

def oddball(stim):
    return True if stim[0] in ['o'] else False

def neg(stim):
    return True if stim[4] in ['E'] and stim[0] in ['R'] else False

def neut(stim):
    return True if stim[4] in ['N'] and stim[0] in ['R'] else False

is_go = lefthand


def genTrialList():
    """ 
    generate trial list for empathyp
    equal number of 
	"""
    #------------------------------------------------------------------------
    # read stim file name in folder
    #------------------------------------------------------------------------
    for root, dirs, files in os.walk('Stimuli'): stimList = files
    random.shuffle(stimList)
    #------------------------------------------------------------------------   # categorize stim into go and no go list
    #------------------------------------------------------------------------
    goStim = [stim for stim in stimList if is_go(stim)]
    neutStim = [stim for stim in stimList if neut(stim)]
    negStim = [stim for stim in stimList if neg(stim)]
    oddStim = [stim for stim in stimList if oddball(stim)]
    
    random.shuffle(goStim)
    random.shuffle(neutStim)
    random.shuffle(negStim)
    random.shuffle(oddStim)

    #------------------------------------------------------------------------	# read jitter list
    #------------------------------------------------------------------------
    with open('fMRI_jitter_new.txt') as jitter:
        ISI = jitter.read().splitlines()	

    #------------------------------------------------------------------------
    # define numbers of each type of trials
    #------------------------------------------------------------------------
    nNeg = len(negStim)/4
    nNeut= len(neutStim)/4
    nGo = len(goStim)/4 #(  20% de nNoGo. allows for 8 pictures of each conditions)
    nOdd = len(oddStim)/4

    indstart = 0
    indstop = nNeg
    Go_indstart= 0
    Go_indstop = nGo
    Odd_indstart = 0
    Odd_indstop = nOdd

    for run in range(4):

        writeTrials = csv.writer(open('run' + str(run+1) + '.csv','wb'), delimiter = ',', quotechar = '"')
        header = ['Run', 'Stim', 'Condition', 'ITI']
        writeTrials.writerow(header)
        
        #------------------------------------------------------------------------	
        # create list of desired amount of each type of Trials   
        #-----------------------------------------------------------------------

        # mix Go and No Go
        
        trials = [GO] * nGo
        trials += [NEG] * nNeg
        trials += [NEUT]* nNeut
        trials += [ODDBALL] * nOdd
        #trials += [NULL]*nNull
        random.shuffle(trials)
        
        #---------------------------------
        # Create stimuli list for this run
        #---------------------------------
       
        Neg_run = negStim[indstart:indstop]
        Neut_run = neutStim[indstart:indstop]
        indstart += nNeg
        indstop += nNeg
        print indstart
        print indstop

        Go_run = goStim[Go_indstart:Go_indstop]
        Go_indstart += nGo
        Go_indstop += nGo
        
        
        
        Odd_run = oddStim[Odd_indstart:Odd_indstop]
        Odd_indstart += nOdd
        Odd_indstop += nOdd
        
        print Neg_run, Neut_run, Go_run, Odd_run
        # insert regular null event for resting control condition
        for i in range (1, len(trials)+len(trials)/6,6):
            trials.insert(i, NULL)	
            

        # then insert PAUSE (hypnosis reinforcement) 
       # for i in range(1,len(trials), len(trials)/2):
        #    if i != 1:
        #      trials.insert(i,PAUSE) 
        
        #------------------------------------------------------------------------
        # create list of trials
        #------------------------------------------------------------------------
        ind_run = str(run+1)
        indGo = 0
        indNeg = 0
        indNeut= 0
        indOdd = 0
        indNull = 0
        trial = [] 
        
        for i in range(len(trials)):
            if trials[i] == 3:
                stim   = Odd_run[indOdd]
                trial  = [ind_run, stim ,'oddball', str(ISI[i])]
                indOdd +=1
            elif trials[i] == 5:
                trial = [ind_run, 'blank', 'blank', 5]

            elif trials[i] == 4:
                trial = ['pause', 'pause']

            elif trials[i] == 2: 	
                stim = Neg_run[indNeg]
                trial = [ind_run, stim,'neg',str(ISI[i])]
                indNeg += 1
            elif trials[i] == 6: 	
                stim = Neut_run[indNeut]
                trial = [ind_run, stim,'neut',str(ISI[i])]
                indNeut += 1
                
            elif trials[i] == 1:	
                stim = Go_run[indGo]
                trial = [ind_run, stim,'go',str(ISI[i])]
                indGo += 1
            writeTrials.writerow(trial)

	



#genTrialList(305, 1)
genTrialList()	
