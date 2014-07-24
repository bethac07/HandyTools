# -*- coding: utf-8 -*-
"""
Created on Wed Oct 02 19:18:36 2013

@author: Beth Cimini
Time to write first night: 5 hrs 10 min
Time to bug smash:
"""

from uncertainties import ufloat
from uncertainties.umath import *
import csv
import xlwt
import easygui as eg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def RocheRTPCR():
    book=xlwt.Workbook()
    sheet=book.add_sheet('sheet')
    count=0
    whichfile=eg.fileopenbox('Where is your input file?')
    a=open(whichfile,'r')
    b=csv.reader(a,delimiter='\t')
    cpdict={}
    treatdict={}
    primerdict={}
    columndict={}
    rowdict={}
    itstime=False
    sheetwidthcount=0
    for i in b:
        #i=list(i)
        #print i
        if itstime!=False:
            splitname=i[namecol].split(',')
            thistrip=[]
            rowsinthistrip=[]
            colsinthistrip=[]
            for j in range(len(splitname)):
                thiswell=splitname[j]
                thiswell=thiswell.strip()
                thisrow=thiswell[0]
                if thisrow not in rowsinthistrip:
                    rowsinthistrip.append(thisrow)
                thiscol='%.2d' %int(thiswell[1:])
                if thiscol not in colsinthistrip:
                    colsinthistrip.append(thiscol)
                thistrip.append(thisrow+thiscol)
            thistrip=str(tuple(thistrip))
            if len(rowsinthistrip)>1:
                rowsinthistrip=str(tuple(rowsinthistrip))
            else:
                rowsinthistrip=str(rowsinthistrip[0])
            if len(colsinthistrip)>1:
                colsinthistrip=str(tuple(colsinthistrip))
            else:
                colsinthistrip=str(colsinthistrip[0])
            if rowsinthistrip not in rowdict.keys():
                rowdict[rowsinthistrip]=[thistrip]
            else:
                rowdict[rowsinthistrip].append(thistrip)
            if colsinthistrip not in columndict.keys():
                columndict[colsinthistrip]=[thistrip]
            else:
                columndict[colsinthistrip].append(thistrip)
            
            cpdict[thistrip]=ufloat(i[meancol],i[stdevcol])
            #print 'Not yet'
        #print 'rowdict', rowdict, 'coldict',columndict
        for j in range(len(i)):
            if 'Samples' in i[j]:
                namecol=j
                itstime=True
            if 'MeanCp' in i[j]:
                meancol=j
            if 'STD Cp' in i[j]:
                stdevcol=j
            sheet.row(count).write(j,i[j])
            if j>sheetwidthcount:
                sheetwidthcount=j
        count+=1
    #print sheetwidthcount    
    #Name primer sets and conditions
    treatprimersok=False
    while treatprimersok==False:
        treatments, primers=eg.multenterbox(msg="Enter all of your treatment groups (NOT including -RT) and primer set names, separated by commas.  Don't use any dashes in the names.",fields=['Treatment groups (ie no virus, scramble)','Primer sets (ie GAPDH, B2M)'])
        treatlist=treatments.split(',')
        for i in range(len(treatlist)):
            treatlist[i]=treatlist[i].strip()
            treatlist[i]=treatlist[i].replace('-','')
        primerlist=primers.split(',')
        for i in range(len(primerlist)):
            primerlist[i]=primerlist[i].strip()
            primerlist[i]=primerlist[i].replace('-','')
        aretpok=eg.ynbox(msg='For your list of treatments I have '+str(treatlist)+' and for your list of primers I have '+str(primerlist)+'. Is that right?')
        if aretpok:
            treatprimersok=True
        else:
            treatprimersok=False
    
    treatprimerlookup={}
    for i in treatlist:
        treatdict[i]={}
        for j in primerlist:
            treatdict[i][str(j)]=str(i)+'-'+str(j)
            if j not in primerdict.keys():
                primerdict[j]={str(i):str(i)+'-'+str(j)}
            else:
                primerdict[j][str(i)]=str(i)+'-'+str(j)
            treatprimerlookup[str(i)+'-'+str(j)]=(i,j)
    treatprimecombo=treatprimerlookup.keys()
    treatprimecombo.sort()
    #Figure out which things we're actually analyzing
    finallist=eg.multchoicebox(msg='Which of the following combinations of treatments and primer sets are we analyzing right now?',choices=treatprimecombo)
    #print 'primerdict', primerdict,'treatdict', treatdict
    #print whichdone,finallist,treatdict,primerdict
    while len(finallist)>len(cpdict.keys()):
        finallist=eg.multchoicebox(msg="Whoops! You've listed more conditions than you have sets of CPs.  Which of these are we really doing?",choices=finallist)
    finallist.sort()
    keysort=cpdict.keys()
    keysort.sort()
    mappeddict={}
    
    #Map wells to treatments
    autogen=eg.ynbox('Do you want to try to automatedly map your plate?' )
    if autogen:
        primersinrows=eg.indexbox('Are primer sets in rows or columns?',choices=['Rows','Columns'])
        primermapping={}
        treatmapping={}
        collist=columndict.keys()
        collist.sort()
        #print 'collist', collist
        rowlist=rowdict.keys()
        rowlist.sort()
        #print 'rowlist', rowlist
        if primersinrows==0:
            for i in primerdict.keys():
                primermapping[i]=[]
                whichrow=eg.multchoicebox('Which row or rows are primer '+i+'?',choices=rowlist)
                for j in whichrow:
                    primermapping[i]+=rowdict[j]
            for i in treatdict.keys():
                treatmapping[i]=[]
                whichcol=eg.multchoicebox('Which column or columns are treatment '+i+'?',choices=collist)
                for j in whichcol:
                    treatmapping[i]+=columndict[j]
        else:
            for i in primerdict.keys():
                primermapping[i]=[]
                whichcol=eg.multchoicebox('Which column or columns are primer '+i+'?',choices=collist)
                for j in whichcol:
                    primermapping[i]+=columndict[j]
            for i in treatdict.keys():
                treatmapping[i]=[]
                whichrow=eg.multchoicebox('Which row or rows are treatment '+i+'?',choices=rowlist)
                for j in whichrow:
                    treatmapping[i]+=rowdict[j]
        #do the mapping
        #print 'primermapping', primermapping, 'treatmapping', treatmapping
        for i in finallist:
            thistreat,thisprimer=treatprimerlookup[i]
            #print thistreat, thisprimer,treatprimerlookup[i]
            for j in primermapping[thisprimer]:
                if j in treatmapping[thistreat]:
                    mappeddict[i]=j
                    break
        
        readablemapped=mappeddict.items()
        for i in range(len(readablemapped)):
            readablemapped[i]=str(readablemapped[i])
        readablemapped.sort()
        eg.textbox(msg="This is the mapping I've automatically generated. The next window will ask you if it's right.  If it's not, we'll manually set up the mapping",text='\n'.join(readablemapped))
        if eg.ynbox(msg='Was the mapping on the previous page correct?'):
            for i in mappeddict.keys():
                mappeddict[i]=cpdict[mappeddict[i]]
        else:
            mappeddict={}
    #If the user doesn't want to automate or if the automation fails:
    if len(mappeddict.keys())==0:
        for i in finallist:
            whichset=eg.choicebox('Which of these sets of wells is '+i+'?',choices=keysort)
            mappeddict[i]=cpdict[whichset]
            keysort.remove(whichset)
    
    #Figure out how we're normalizing and where we're saving
    negctl=eg.choicebox('Which of these treatments are we normalizing by?',choices=treatdict.keys())
    housekeeping=eg.choicebox('Which of these primers is our housekeeping gene?',choices=primerdict.keys())
    tosave=eg.filesavebox('Where do you want to save the output file?')
    if '.' in tosave:
        tosave=tosave[:tosave.index('.')]
    
    """rmalize by -RT    
    for i in mappeddict.keys():
        if i in hasRT:
            #mappeddict[i]=some math related to mappeddict[i] and mappeddict[i+' no RT']
            mappeddict.pop(i+' no RT')"""
    
    #Normalize by housekeeping gene
    for i in treatdict.keys():
        normbyhouse=mappeddict[treatdict[i][housekeeping]]
        for j in treatdict[i]:
            pass
            mappeddict[treatdict[i][j]]=mappeddict[treatdict[i][j]]-normbyhouse
    
    #Normalize by negative control
    for i in primerdict.keys():
        normbyneg=mappeddict[primerdict[i][negctl]]
        for j in primerdict[i]:
            mappeddict[primerdict[i][j]]=2**(-(mappeddict[primerdict[i][j]]-normbyneg))
            pass
        
    
    
    finalkeylist=mappeddict.keys()
    finalkeylist.sort()
    rowcount=1
    sheetwidthcount+=1
    sheet.write(0,sheetwidthcount,'Treatment Name+Primer Name')
    sheet.write(0,sheetwidthcount+1,'Fold Change')
    sheet.write(0,sheetwidthcount+2,'Standard Deviation')
    for i in range(len(finalkeylist)):
        sheet.write(rowcount,sheetwidthcount,finalkeylist[i])
        sheet.write(rowcount,sheetwidthcount+1,mappeddict[finalkeylist[i]].nominal_value)
        sheet.write(rowcount,sheetwidthcount+2,mappeddict[finalkeylist[i]].std_dev)
        rowcount+=1
        
    
    #Make graphs
    
    book.save(tosave+'.xls')
    histPDF=PdfPages(tosave+'.pdf')
    width=0.4
    sortedprimers=primerdict.keys()
    sortedprimers.sort()
    histdic={}
    for i in sortedprimers:
        if i!=housekeeping:
            listoflocs=[]
            listofvals=[]
            listoferrors=[]
            tickplacement=[]
            treatments=primerdict[i].keys()
            treatments.sort()
            treatments=[negctl]+treatments[:treatments.index(negctl)]+treatments[treatments.index(negctl)+1:]
            for j in range(len(treatments)):
                listoflocs.append(j)
                tickplacement.append(j+0.5*width)
                listofvals.append(mappeddict[primerdict[i][treatments[j]]].nominal_value)
                listoferrors.append(mappeddict[primerdict[i][treatments[j]]].std_dev)
            histdic[i]={'treatments':treatments,'values':listofvals,'errors':listoferrors}
            plt.ioff()
            plt.figure()
            plt.bar(listoflocs,listofvals,yerr=listoferrors,error_kw={'ecolor':'black'},width=width,color='LightSlateGray')
            
            plt.ylabel('Relative expression')
            plt.title('Relative expression of '+i)
            plt.xticks(tickplacement, treatments,fontsize='xx-small',rotation=45 )
            plt.legend([i])
            plt.savefig(histPDF, format='pdf')
    histdickeys=histdic.keys()
    histdickeys.sort()
    firstprimertreats=histdic[histdickeys[0]]['treatments']
    allvals=histdic.values()
    allvalset=[]
    for i in allvals:
        #print i
        if i['treatments'] not in allvalset:
            allvalset.append(i['treatments'])
    #print allvalset        
    if len(allvalset)==1:
        count=0
        finalwidth=0.8/len(histdickeys)
        #print finalwidth
        xvalstart=range(len(firstprimertreats))
        xticks=list(xvalstart)
        for i in range(len(xticks)):
            xticks[i]+=0.4
        plt.ioff
        plt.figure()
        ax=plt.subplot(111)
        for i in range(len(histdickeys)):
            colorlist=['r','b','g','y','LightSlateGray','m','c','Sienna','DeepPink','Lime']
            xvals=list(xvalstart)
            for j in range(len(xvals)):
                xvals[j]+=count*finalwidth
            ax.bar(xvals,histdic[histdickeys[i]]['values'],yerr=histdic[histdickeys[i]]['errors'],error_kw={'ecolor':'black'},width=finalwidth,color=colorlist[count%10])
            count+=1
        plt.ylabel('Relative expression')
        plt.title('Relative expression of all primers examined')
        plt.xticks(xticks,allvalset[0],fontsize='xx-small',rotation=45)
        box=ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        # Put a legend to the right of the current axis
        #plt.legend(histdickeys)
        leg=ax.legend(histdickeys,loc='center right', bbox_to_anchor=(1.3, 0.5))
        #ax.legend(histdickeys)
        plt.savefig(histPDF, format='pdf')         
            
    histPDF.close()
    #book.save(r'G:\trash.xls')

if __name__=='__main__':
    keepgoing=True
    while keepgoing==True:
        RocheRTPCR()
        if eg.ynbox('Do you want to do another?'):
            keepgoing=True
        else:
            keepgoing=False

