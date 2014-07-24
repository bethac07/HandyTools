# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 14:41:04 2014

@author: Beth
"""
import matplotlib.pyplot as plt
import easygui
import os

def drawwells(numwells,xcoords,ycoords,xlim=(40,10),ylim=(75,-10),xline=25,ylines=[],manual=False):
    plt.close()
    plt.ioff()
    plt.figure()
    halfwells=int(numwells/2)
    if manual==False:
        plt.xlim(xlim[0],xlim[1])
        plt.ylim(ylim[0],ylim[1])
        plt.plot([25,25],[ylim[0],ylim[1]])
        plt.text(25,ylim[1],"1") 
        for i in range(1,halfwells):
            plt.plot([xlim[0],xlim[1]],[-10+(85*i/halfwells),-10+(85*i/halfwells)])
            plt.text(8,-10+(85*i/halfwells),str(i+1))
    else:
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.plot((xline,xline),ylim)
        plt.text(xline,ylim[1]-1,"1")
        if ylines==[]:
          for i in range(1,halfwells):
            plt.plot(xlim,[ylim[1]+((ylim[0]-ylim[1])*i/halfwells),ylim[1]+((ylim[0]-ylim[1])*i/halfwells)])
            plt.text(xlim[1]-1,ylim[1]+((ylim[0]-ylim[1])*i/halfwells),str(i+1))
        else:
            for i in range(len(ylines)):
                plt.plot(xlim,[ylines[i],ylines[i]])
                plt.text(xlim[1]-1,ylines[i],str(i+2))
    plt.plot(xcoords,ycoords,'b+',markersize=8)
    plt.show(block=False)
    #print xcoords,ycoords
    
def idwells(numwells,xcoords,ycoords,xline,ylines,xlim=(40,10),ylim=(75,-10)):
    plt.close()
    plt.ioff()
    plt.figure()
    halfwells=int(numwells/2)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks([])
    plt.yticks([])
    plt.plot((xline,xline),ylim)
    for i in range(len(ylines)):
        plt.plot(xlim,[ylines[i],ylines[i]])
        plt.text(xlim[1]-1,ylines[i]+5,str(i+1))
        plt.text(xlim[0]+1,ylines[i]+5,str(i+1+halfwells))
    plt.text(xlim[1]-1,ylim[1]+5,str(halfwells))
    plt.text(xlim[0]+1,ylim[1]+5,str(halfwells*2))
    plt.plot(xcoords,ycoords,'r+',markersize=3)
    plt.show(block=False)

def metasystemsid():
        directory=easygui.diropenbox()
        files=os.listdir(directory)
        filedict={}
        chanlist=[]
        for i in files:
            if '.TIF' in i.upper():
                if os.path.isfile(os.path.join(directory,i)):
                    tilde=i.index('~')
                    filenum=i[tilde+3:-4]
                    #print filenum
                    slideheader=i[:tilde]
                    if filenum not in filedict.keys():
                        filedict[filenum]=[i]
                    else:
                        filedict[filenum]+=[i]
        #print len(filedict.keys()),'filedict'
        #print filedict        
        locdict={}
        xcoords=[]
        ycoords=[]
        coordfile=easygui.fileopenbox('Where is the file with the list of coordinates?')
        opencoord=open(coordfile,"rb")
        hasperiod=[]
        for eachline in opencoord:
            if '.' in eachline:
                if 'Ref' not in eachline:
                    hasperiod.append(eachline)
        for eachline in hasperiod:
            spaces=[]
            lastspaces=[]
            firstnonspace=False
            for j in range(len(eachline)-1):
                if eachline[j]==' ':
                    spaces.append(j)
                else:
                    if firstnonspace==False:
                        firstnonspace=j
            for eachspace in spaces:
                if eachspace+1 not in spaces:
                    if eachspace>firstnonspace:
                        lastspaces.append(eachspace)
            #print "spaces", spaces, "lastspaces", lastspaces
            try:
                identcode=int(eachline[:lastspaces[0]])
                ycode=float(eachline[lastspaces[1]:lastspaces[2]])
                xcode=float(eachline[lastspaces[2]:lastspaces[3]])
                locdict[identcode]=(xcode,ycode)
            except:
                print eachline
                pass
        #print len(locdict.keys()), "locdict"
        for i in filedict.keys():
            """something to get the list of coordinates"""
            coordinates=locdict[int(i)]
            xcoords.append(coordinates[0])
            ycoords.append(coordinates[1])
        #print locdict
        intwells=False
        while intwells==False:
            try:
                numwells=easygui.enterbox(msg='How many wells did the chamber slide have?')
                numwells=int(numwells)
                halfwells=int(numwells/2)
                intwells=True
            except:
                pass
            
        vertdiv=25
        hordiv=[]
        for i in range(1,halfwells):
            hordiv.append(-10+(85*i/halfwells))
            
        drawwells(numwells,xcoords,ycoords,xlim=(max(xcoords),min(xcoords)),ylim=(max(ycoords),min(ycoords)))
        if easygui.ynbox('Do you need to move any of the dividing lines?'):
            wellsright=False
            while wellsright==False:
                tochange=easygui.indexbox('Which dividing line do you want to move?',choices=range(1,halfwells+1))
                if tochange==0:          
                    vertnum=False
                    while vertnum==False:
                        try:
                           vertemp=easygui.enterbox('What do you want the coordinate for line 1 to be?') 
                           vertdiv=float(vertemp)
                           vertnum=True
                        except:
                            pass
                else:
                    hornum=False
                    while hornum==False:
                        try:
                            hortemp=easygui.enterbox('What do you want the coordinate for line '+str(tochange+1)+' to be?')
                            hortemp=float(hortemp)
                            hordiv[tochange-1]=hortemp
                            hornum=True
                        except:
                            pass
                drawwells(numwells,xcoords,ycoords,manual=True,xline=vertdiv,ylines=hordiv)
                if easygui.ynbox('Do you need to move any of the dividing lines?'):
                    wellsright=False
                else:
                    wellsright=True
        plt.close()
        hordiv.sort(reverse=True)
        idwells(numwells,xcoords,ycoords,vertdiv,hordiv)
        treatments=easygui.multenterbox(msg='What are the names of the treatment in each well? Leave blank if there are no cells in that well.',fields=range(1,numwells+1))
        
        plt.close()
        treatmap={}
        for j in range(len(treatments)):
            if treatments[j]!="":
                treatmap[j+1]=os.path.join(directory,treatments[j])
                if os.path.isdir(treatmap[j+1])!=True:
                    os.mkdir(treatmap[j+1])
        print treatmap
        for i in filedict.keys():
            #print filedict[i]
            x,y=locdict[int(i)]
            maxy=[max(ycoords)+1]
            maxy+=hordiv            
            for j in range(len(maxy)):
                if y<maxy[j]:
                    foundwell=j+1
            if x<vertdiv:
                for eachfile in filedict[i]:
                    os.rename(os.path.join(directory,eachfile),os.path.join(treatmap[foundwell],eachfile))
            else:
                for eachfile in filedict[i]:
                    os.rename(os.path.join(directory,eachfile),os.path.join(treatmap[foundwell+halfwells],eachfile))

if __name__=="__main__":
    again=True
    while again==True:
        metasystemsid()
        again=easygui.ynbox('Do you want to do another?')
        