# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 13:12:28 2012

@author: Beth Cimini
"""
from numpy import random
import os
import easygui as eg
import xlwt

def fixname():
    bname=r'D:\ASUSWebStorage\20131204'
    b=os.listdir(bname)
    count=0
    for i in b:
        if 'bmp' in i:
            newname='UDay7_'+i
            #newname=i[:6]+i[15:-17]+'H2AX'+i[-18:]
            #print i, newname
            os.rename(os.path.join(bname,i),os.path.join(bname,newname))
            count+=1
    print count

def appendrand(directory,common='.tif',length=3,n=300):
    files=os.listdir(directory)
    for i in files:
        if common in i:
            number="%0*d" %(length,random.randint(0,n))
            os.rename(os.path.join(directory,i),os.path.join(directory,number+i))

def removerand(directory,common='D3D',length=3):
    files=os.listdir(directory)
    for i in files:
        if common in i:
            os.rename(os.path.join(directory,i),os.path.join(directory,i[length:]))

def removeend(common='Out',length=-3):
    masterfolder=eg.diropenbox(msg='Which is the master folder?')
    recurselevels=eg.enterbox('How many sublevels do you want to recurse?')
    try:
        recurselevels=int(recurselevels)
    except:
        recurselevels=eg.enterbox('How many sublevels do you want to recurse?-Please enter a number this time')
    #common=eg.enterbox(msg='What common text do you want to use to empty folders?')
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
        files=os.listdir(i)
        for j in files:
            if common in j:
                os.rename(os.path.join(masterfolder,i,j),os.path.join(masterfolder,i,j[:length]))
                
def randomizer():
    folder=eg.diropenbox('Where are the files you want to randomize?')
    files=os.listdir(folder)
    foldname=os.path.split(folder)[1]
    workbook=xlwt.Workbook()
    name=foldname+" randomization"
    while len(name)>=31:
        name=eg.enterbox("Filename "+name+" is too long- enter a shorter one")
    randsheet=workbook.add_sheet(name)
    rowcount=0
    numberlist=[]
    for i in files:
        number="%0*d" %(4,random.randint(0,len(files)*3))
        while number in numberlist:
            number="%0*d" %(4,random.randint(0,len(files)*3))
        randsheet.write(rowcount,0,number)
        randsheet.write(rowcount,1,i)
        os.rename(os.path.join(folder,i),os.path.join(folder,number+'.tif'))
        rowcount+=1
        numberlist.append(number)
    workbook.save(os.path.join(folder,name+'.xls'))
    
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


#fixname()
#appendrand(r'D:\20140331')
removerand(r'D:\20140331')
#removeend()
#randomizer()