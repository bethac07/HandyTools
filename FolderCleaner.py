# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:40:50 2012

@author: Beth Cimini
"""

import easygui as eg
import os

def foldercleaner():
    masterfolder=eg.diropenbox(msg='Which is the master folder?')
    recurselevels=eg.enterbox('How many sublevels do you want to recurse?')
    try:
        recurselevels=int(recurselevels)
    except:
        recurselevels=eg.enterbox('How many sublevels do you want to recurse?-Please enter a number this time')
    textforcleanup=eg.enterbox(msg='What common text do you want to use to empty folders?')
    maybecleaned=[]
    allsubfolders=[masterfolder]
    recursions=0
    while recursions<recurselevels:
        templist=[]
        for h in allsubfolders:
            for i in os.listdir(h):
                subthingname=os.path.join(h,i)
                if os.path.isdir(subthingname):
                    templist.append(subthingname)
        allsubfolders+=templist
        recursions+=1
    for i in allsubfolders:
        if textforcleanup in i:
            maybecleaned.append(i)
    willbecleaned=eg.multchoicebox('Confirm which of these folders you want to be emptied.  This is your last chance to make changes.',choices=maybecleaned)
    for i in willbecleaned:
        for root, dirs, files in os.walk(i, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def foldermaker():
    masterfolder=eg.diropenbox(msg='Which is the master folder?')
    recurselevels=eg.enterbox('How many sublevels do you want to recurse?')
    try:
        recurselevels=int(recurselevels)
    except:
        recurselevels=eg.enterbox('How many sublevels do you want to recurse?-Please enter a number this time')

    allsubfolders=[masterfolder]
    recursions=0
    while recursions<recurselevels:
        templist=[]
        for h in allsubfolders:
            for i in os.listdir(h):
                subthingname=os.path.join(h,i)
                if os.path.isdir(subthingname):
                    templist.append(subthingname)
        allsubfolders+=templist
        recursions+=1
    willbecleaned=eg.multchoicebox('Which of these folders you want to make a paired version of?',choices=allsubfolders)
    texttoadd=eg.enterbox(msg='What common text do you want to append to each folder?')    
    for i in willbecleaned:
        os.mkdir(i+texttoadd)
            
            
if __name__=='__main__':
    #foldercleaner()
    #foldermaker()