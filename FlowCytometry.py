# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:59:25 2012

@author: Beth Cimini
"""

import easygui
import os
import csv
import matplotlib.pyplot as plt

class flowcells(object):
    pass
            
def graphhistforflow(valuelist,title,saveas,xlabel='This axis is wrong',size=(480,480),axes=None,manlines=None):
    plt.ioff() #turn off interactive mode to run more quickly
    plt.figure() #start a new figure
    plt.hist(valuelist,100,normed=False,histtype='stepfilled',color='black') #create a 20-binned histogram <---------More parameters can be changed here if desired
    plt.title(title) #title the histogram with what it is
    plt.xlabel(xlabel)
    plt.ylabel('Count')
    if axes!=None:
        plt.axis(axes)
    if manlines!=None:
        for i in manlines:
            plt.plot(i[0],i[1],color='red')
    #plt.show()
    plt.savefig(saveas+'.png') #save and close the .png
    plt.close()

def readflowcsvs(filename):
    a=csv.reader(open(filename,'rb'),delimiter='\t')
    container=[]
    for row in a:
        container.append(row[1:-1])
    rawheadings=container.pop(0)
    headings=[]
    for i in rawheadings:
        if '-' in i:
            dash=i.index('-')
            headings.append(i[:dash]+i[dash+1:])
        else:
            headings.append(i)
    celldict={}
    for i in range(len(container)):
        a=flowcells()
        for j in range(len(headings)):
            setattr(a,headings[j],int(container[i][j]))
        celldict[i]=a
    return celldict

def runflowhists(param,minval=0,maxval=9999999999999,axes=None,manlines=None):
    dirname=easygui.diropenbox()
    txtfiles=[]
    for i in os.listdir(dirname):
        if '.txt' in i:
            txtfiles.append(i)
    files=easygui.multchoicebox('Which of these do you want to graph',choices=txtfiles)
    for eachfile in files:
        filename=os.path.join(dirname,eachfile)
        data=readflowcsvs(filename)
        listofvalues=[]
        for i in data.values():
            if getattr(i,'FSCH')>=180:            
                a=getattr(i,param)
                if a>=minval:
                    if a<=maxval:
                        listofvalues.append(a)
        #print len(listofvalues)
        graphhistforflow(listofvalues,eachfile[:-4]+'-'+param,filename[:-4]+param,xlabel=param,axes=axes,manlines=manlines)

if __name__=='__main__':
    runflowhists('FL4H',minval=-1,maxval=9000,axes=[0,1100,0,3500],manlines=[[[130,130],[0,3500]],[[240,240],[0,3500]]])


#class spots(list):
#    def __init__(self,filename,movielen,minlength=0):
#        """Read an Excel file, pick out all the 
#        instances of a given spot (as identified by Label)
#        and give them a list of all the attributes measured
#        The overall container is a list, with the headings as
#        index 0 and the rest of the spots in order as lists of lists
#        (one list for each timepoint, containing all the data
#        from that timepoint)
#        minlength allows the user to gate out instances that 
#        don't persist for a certain length of time"""
#        
#        
#        array=numpy.genfromtxt(filename,delimiter=',',dtype=None)
#        array2=numpy.genfromtxt(filename,delimiter=',',dtype=numpy.float64)
#        headings=list(array[0,:]) #read headings
#        
#        
#        self.append(headings) #save headings to self
#        for i in range(len(headings)): #identify the label column
#            if 'TrackObjects_Label' in headings[i]:
#                labelcolumn=i