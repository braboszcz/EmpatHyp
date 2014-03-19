from psychopy import visual, core, data, event
from numpy.random import shuffle
import copy, time
import rating_pain as rp
#import msa

#expInfo = {'subject:' 'session:'}

#inifile = '365_Thermod_v5_fmri_v.6_748_130827.ini';
#port = MsaOpen(1,inifile)   #4;
#MsaMonitor(1);
#MsaSetTemp(45)

#make a text file to save data
#fileName = expInfo['subject'] + expInfo['session']
#dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
#dataFile.write('temperature, rating\n')

win = visual.Window([800,600])

### Thermode settings
TBase = 37 #baseline temp
TStartMin = 40 # starting temperature
TStartMax = TStartMin+4 #maximum possible baseline temp
BigChange = 2 # temperature changes for two identical consecutive resp
SmallChange = 1 #temperature changes for different consecutive resp 
trial_dur = 2 #duration (sec)
raise_dur = 3 # how much time (Sec)
slope = 4 # time to get to temperature

max_time = 8

#---Staircase settings----#
info = {}
info['subject']= 'test'
info['session'] = 'norm'
nTurn = 3 # number of turning point
nStair = 2 # number of multiple random staircase
critical_resp = 2 # critical threshold turning point

startPoints={}
for stairN in range(nStair):
    startPoints[stairN]= (TStartMin+((TStartMax-TStartMin)/nStair)*(stairN))

info['startPoints']=startPoints
info['nTrials']=1

#create staircasei
resp = 0

prev_resp = 0
stairs =[]

for thisStart in info['startPoints']:
    thisInfo= copy.copy(info) #copy of expinfo for each staircase
    thisInfo['thisStart']=thisStart
    thisStair = data.StairHandler(startVal=
          thisInfo['startPoints'][thisStart], extraInfo = thisInfo, nReversals=nTurn, nUp=1, nDown=1, stepType = 'lin', minVal=37, maxVal=52, stepSizes=[BigChange, SmallChange], nTrials = 15)
    stairs.append(thisStair)


#for trialN in range (info['trials']): # change trial value
endThresh = 0 # detection of threshold marker
addChange = 0
get_critic = 0

for trialN in range(info['nTrials']):
#while endThresh == 0:
     shuffle(stairs)
     for thisStair in stairs:
        thisTemp=thisStair.next()
        #thisStair.stepSizes = thisStepSize
        print 'start temp= %.2f,  current temperature= %.2f' %(thisInfo['startPoints'][thisStart], thisTemp) 
        
        #---- run trial and get input ----#
        resp = rp.rate_pain(win, max_time)
        print resp

        #----------------------------------------------
        #is the rating smaller than critical response ?
        #----------------------------------------------
        if resp >= critical_resp:
           # get_critic = 0 # rating higher than critic resp
            critic_value = False
        else:
            #get_critic = 1 #rating smaller than critic resp
            critic_value = True

        #if get_critic == prev_resp: 
        #    if get_critic == 0: # critical value not crossed
        #    else:               # critical value crossed
        #   
        #    critic_value =False
        #    print 'seuil critique' = critic_value 
        #else:
        #    if get_critic == 1:
        #        thisStepSize = -SmallChange
        #    else:
        #        thisStepSize = SmallChange    
        #    
        #    critic_value=True
        print  critic_value 
        thisStair.addData(critic_value) # so that the staircase adjust itself
        #end trial
# end of all trials
#----------------------------
#Compute online Threshold
#------------------------------


#save dataFile
#datStr = time.strftime('%b_%d_%H%M, time.localtime())') # add current time
for thisStair in stairs:
    filename = "%s, %s"(thisStair.extraInfo['subject'], thisStair.extraInfo['session'])
    #thisStair.saveAsPickle(filename)
    thisStair.saveAsText(filename)

