# -*- coding: utf-8 -*-
"""
Created on Tue May 14 20:52:40 2013

@author: Beth Cimini
"""

import os

def musicduplicatecleaner(musicdir):
    count=0
    for root, dirs, files in os.walk(musicdir, topdown=False):
            for name in files:
                #print name
                if name[:-8]+name[-4:] in files:
                    os.remove(os.path.join(root,name))
                    #print os.path.join(root,name)
                    count+=1
    print count
    
musicduplicatecleaner(r'C:\Users\Beth Cimini\Pictures')
