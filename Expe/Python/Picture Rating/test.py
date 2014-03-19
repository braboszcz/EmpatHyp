# -*- coding: utf8 -*-
#!/usr/bin/env python

from psychopy import visual, event, core, logging, data
import os
import random

#Experiment handler

# create a window before creating your rating scale, whatever units you like:
myWin = visual.Window(fullscr=True, units='pix', monitor='testMonitor', color='white')

# instructions from the subject's point of view:

instr = visual.TextStim(myWin, text="""Pour chacune des images qui vous suivantes, notez successivement \n 1. votre niveau de familiarite avec le contenu de l' image \2.l'intensite de la douleur devant etre ressentie dans l' image""", color=(0,0,0))
instr.draw()
myWin.flip()
if 'escape' in event.waitKeys():
    core.quit()

im_dir = 'Stimuli'
im_size = 600, 600

# create a scale for Example 2, using quite a few non-default options:
myRatingScale = visual.RatingScale(myWin, low=1, high=10, precision=1, 
        markerStyle='triangle',markerStart= 5,  showValue=True, allowSkip=False, pos=[0,-350], name='Familiarity', textColor= 'black', lineColor = 'black',displaySizeFactor=0.85, stretchHoriz=1.5 )

# using a list is handy if you have a lot of items to rate on the same scale, eg personality adjectives or images:
imageList = [f for f in os.listdir(im_dir)] # find all .png or .jpg images in the directory
imageList = imageList[:1] # ...but lets just use the first two
random.shuffle(imageList)

#thisExp = data.ExperimentHandler(name='ratings', version= ' ', runtimeInfo=None, originPath=None, savePickle=False, saveWideText=False) 
#trials = data.TrialHandler(imageList, nReps=1, method='sequential')
#trials.data.addDataType('Image')
#trials.data.addDataType('Condition')
#trials.data.addDataType('Rating')
#trials.data.addDataType('RT')
#print trials
#trials.saveAsWideText('test.csv', delim=',', appendFile=True)
#for thisTrial in trials:
    #x,y = myRatingScale.win.size
  #  trials.saveAsWideText('test.csv', delim=',', appendFile=True)
   # rating = []
   # myItem = visual.SimpleImageStim(win=myWin, image= os.path.join(im_dir,thisTrial), units='pix', pos=[0, y/9])
data=[]
for image in imageList: 
    x,y = myRatingScale.win.size
    myItem = visual.ImageStim(win=myWin, image= os.path.join(im_dir,image), units='pix', pos=[0, y/9], size=(im_size))
    
    # rate each image on two dimensions
    for dimension in ['0=totalement inconnu..........10=tres familier', '0= extremement douloureux.........10=pas du tout douloureux']:
        myRatingScale.reset() # needed between repeated uses of the same rating scale
        myRatingScale.setDescription(dimension) # reset the instructions for this rating
        event.clearEvents()
        while myRatingScale.noResponse:
            myItem.draw()
            myRatingScale.draw()
            myWin.flip()
       
       # trials.addData('Image', thisTrial)
       # trials.addData('Condition', myRatingScale.scaleDescription.text)
       # trials.addData('Rating',myRatingScale.getRating())
       # trials.addData('RT', myRatingScale.getRT())
        data.append([image, myRatingScale.scaleDescription.text, myRatingScale.getRating(), myRatingScale.getRT()]) # save for later
        # clear the screen & pause between ratings
        myWin.flip()
        core.wait(0.35) # brief pause, slightly smoother for the subject
        #trials.next()
for d in data:
    print '  ',d
myWin.close()
