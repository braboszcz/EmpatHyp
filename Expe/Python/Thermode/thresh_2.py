from psychopy import visual, core, data, event
import random
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
n_turn = 3 # number of turning point
n_stair = 2 # number of multiple random staircase
critical_resp = 2 # critical threshold turning point

temperatures={}
for stairN in range(n_stair):
    temperatures[stairN]= (TStartMin+((TStartMax-TStartMin)/n_stair)*(stairN))

#create staircase
resp = 0
prev_resp = [0,0]
stairs =[]
it = 0
###############

prev_temperatures = [0, 0]
count_turn = 0
is_critic = 0

def check_resp(resp, critical_resp):

    if resp >= critical_resp :
        is_critic = False
    else:
        is_critic = True
    return is_critic

def get_next_temp(temp,is_critic,resp, prev_resp, count_turn):
    print resp, prev_resp 
    if resp == prev_resp:
        if is_critic == 0:
            temp += BigChange
        else:
            temp -= BigChange
    else:
        count_turn+=1
        if is_critic == 0:
            temp += SmallChange
        else:
            temp -= SmallChange
    return temp, count_turn



while count_turn < n_turn*n_stair:
    it += 1
    idx = random.choice([0,1])
    temp, count_turn = get_next_temp(temperatures[idx],is_critic, resp, prev_resp[idx],count_turn)
    prev_resp[idx]=resp  
    print 'coucou'  
    print 'temp =', temp
    print 'prev resp', prev_resp[idx] 
    resp = rp.rate_pain(win, max_time)
    
    is_critic = check_resp(resp, critical_resp)
    
    print is_critic
    print 'turn',   count_turn
    temperatures[idx] = temp
   # prev_temperatures[idx] = prev
  



#########
