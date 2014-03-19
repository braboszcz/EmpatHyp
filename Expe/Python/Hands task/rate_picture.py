# -*- coding: utf8 -*-
#!/usr/bin/env python


'''
Rating images used in empathyp

'''


from psychopy import visual, event, core, logging
import os
import random

#---------------------------------------
# Setup the Window
#---------------------------------------
win = visual.Window([1280,1024],color = 'white',monitor ='testMonitor',  units='pix', fullscr = False, colorSpace = 'rgb')

instr = visual.TextStim(win, text= """A quel point le contenu de cette image vous est familier ? """ )

event.clearEvents()
instr.draw()
win.flip()
#if 'q' in event.waitKeys() :
#    core.quit()

# create rating scale
#myRatingScale = visual.RatingScale(win, low = 1, high = 10, markerStart= 5, leftKeys=['left'], rightKeys=['right'], acceptKeys = ['space', 'return'], lowAnchorText='Totalement inconnu', highAnchorText='Extremement familier', markerStyle= 'circle', displaySizeFactor=0.85, showAccept = False, lineColor= 'black', textColor = 'black', precision = 1, stretchHoriz=2 )

myRatingScale = visual.RatingScale(win)
im_dir = 'Stimuli'
im_size = 0.2, 0.2 
imageList = [f for f in os.listdir(im_dir)]
imageList = imageList[:3] # for testing
random.shuffle(imageList)

data = []
for image in imageList:
    x, y = myRatingScale.win.size
    myItem = visual.ImageStim(win = win, image = os.path.join(im_dir, image), units = 'pix', pos=[0, y/9])
    myRatingScale.reset()
    #myRatingScale.setDescription(dimension)
    event.clearEvents()
    while myRatingScale.noResponse:
        myItem.draw()
        myRatingScale.draw()
        win.flip()
        data.append([image, myRatingScale.getRating(), myRatingScale.getRT()])

    #clear screen and pause between ratings
    win.flip()
    core.wait(0.35)
    win.close()
