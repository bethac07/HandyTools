# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:02:28 2013

@author: Beth Cimini
"""

import os
import easygui as eg

def digitpadder(folder=None):
    if folder==None:
        masterfolder=eg.diropenbox(msg='Where are your files?')
    else:
        masterfolder=folder
    allfiles=os.listdir(masterfolder)
    for i in allfiles:
        if '.tif' in i:
            istif=True
        elif '.TIF' in i:
            istif=True
        else:
            istif=False
        if istif==True:
            dots=[]
            for m in range(len(i)):
                if i[m]=='.':
                    dots.append(m)
            for eachdot in range(len(dots)-1):
                betweendots=i[dots[eachdot]+1:dots[eachdot+1]]
                #print betweendots
                try:
                    betweendots=int(betweendots)
                    padded='%03d' %betweendots
                    os.rename(os.path.join(masterfolder,i),os.path.join(masterfolder,i[:dots[eachdot]+1]+padded+i[dots[eachdot+1]:]))
                except:
                    pass

digitpadder()