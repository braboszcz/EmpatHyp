# -*- coding:utf8 -*-
#!/usr/bin/env python

from psychopy import visual, event, core, logging
import os

def rate_pain(win,duration):
   # win = visual.Window(fullscr=True, units='pix', monitor = 'testMonitor')

    event.clearEvents()
    if 'escape' in event.waitKeys():
        core.quit()

    myRatingScale = visual.RatingScale(win, labels=["extremement \n desagreable",'extremement \n agreable'], scale=None,  markerStart=5, leftKeys='1', rightKeys='2', acceptKeys='4', low = 0, high=10, showAccept=False, lineColor= 'Purple', markerColor='Red', marker='circle', size=2,minTime=0.4, maxTime=duration)

    question= 'Comment ressentez-vous cette temperature ?'
    myItem = visual.TextStim(win, text=question, height=.12, units ='norm')

    event.clearEvents()

    while myRatingScale.noResponse:
        myItem.draw()
        myRatingScale.draw()
        win.flip()

    rating = myRatingScale.getRating()
   # print 'history=', myRatingScale.getHistory()
   # print 'rating = ', rating

    return rating
