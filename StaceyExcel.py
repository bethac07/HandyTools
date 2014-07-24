# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 19:31:59 2013

HANLON- High-throughput ANalysis of chromosome Loss after Origin firing in Nocadazole

@author: Beth Cimini
"""
from HandyXLModules import writesheet
import xlrd
import xlwt
import os
import numpy
from scipy import stats
from statsmodels.sandbox.stats.multicomp import multipletests


"""Show 5 vs all others, which chromosomes are thrown out if any- make sure to throw
out the ura locus
then for each cell do a 16x16 matrix comparing all chromosomes- put on a single second sheet
Col 11, 26, 41,...236 against column 71- actually 10, 25, 40...235 against 70 etc"""

sheet1headings=xlwt.easyxf('alignment: wrap true;')
tan = xlwt.easyxf('pattern: fore_colour tan, pattern solid_fill;')
gold = xlwt.easyxf('pattern: fore_colour gold, pattern solid_fill;')
lightorange = xlwt.easyxf('pattern: fore_colour light_orange, pattern solid_fill;')
orange = xlwt.easyxf('pattern: fore_colour orange, pattern solid_fill;')

def allchromcompare(chromdict):
    outarray=[['']]
    pvalarray=[]
    done=[]
    for i in range(1,17):
        outarray[0].append('Chr '+str(i))
        for j in range(1,17):
            if i!=j:
                sortstr=str(numpy.sort([i,j]))
                if sortstr not in done:
                    done.append(sortstr)
                    pvalarray.append(stats.ttest_ind(chromdict[i],chromdict[j],equal_var=False)[1])
    outarray[0]+=['','Chr Mean']
    corrarray=list(multipletests(pvalarray,method='h')[1])
    for i in range(1,17):
        comparrayrow=['Chr '+str(i)]
        for j in range(1,17):
            if j==i:
                comparrayrow.append('**')
            else:
                sortstr2=str(numpy.sort([i,j]))
                #print i,j, sortstr2
                comparrayrow.append(corrarray[done.index(sortstr2)])
        comparrayrow+=['',numpy.mean(chromdict[i])]
        outarray.append(comparrayrow)
    return outarray

def pullexcelarrays(inbook):
    inbook=xlrd.open_workbook(inbook)
    rawsheet=inbook.sheet_by_index(0)
    chromdict={'all':[],'exclude':[]}
    for i in range(16):
        rawfloats=[]
        col=(i*15)+10
        colvalues=rawsheet.col_values(col)
        for j in range(len(colvalues)):
            if type(colvalues[j])==float:
                if i==4:
                    if j==138:
                        pass
                        #print colvalues[j]
                    elif j==139:
                        pass
                        #print colvalues[j]
                    else:
                       rawfloats.append(colvalues[j]) 
                else:
                   rawfloats.append(colvalues[j])
        chromdict[i+1]=rawfloats
        if i!=4:
            if numpy.mean(rawfloats)>1.7:
                if numpy.mean(rawfloats)<2.3:
                    chromdict['all']+=rawfloats
                else:
                    chromdict['exclude'].append(i+1)
            else:
                    chromdict['exclude'].append(i+1)
    return chromdict
        
    

def executechromvfiles(folder):
    writebook=xlwt.Workbook()
    
    vsheet=writebook.add_sheet('Chromosome V vs disomes')
    headings=['Experiment Name','Chromosome V value', 'All other chromosomes value', 'p value','Chromosomes excluded']    
    for i in range(len(headings)): 
        vsheet.col(i).width=4800
        vsheet.write(0,i,headings[i],sheet1headings)
    vrows=1    
    
    allchromsheet=writebook.add_sheet('Compare all chromosomes')
    allchromrows=0
    
    files=os.listdir(folder)
    #print files
    for i in files:
        if '.xls' in i:
            if i[0]!='.':
                print i
                chromdict=pullexcelarrays(os.path.join(folder,i))
                ttest=stats.ttest_ind(chromdict[5],chromdict['all'],equal_var=False)
                #pvalue=ttest[1]
                if ttest[0]<0:
                    pvalue=ttest[1]/2
                else:
                    pvalue=str(ttest[1]/2)+' Greater'
                print pvalue
                row=[str(i),numpy.mean(chromdict[5]),numpy.mean(chromdict['all']),pvalue,str(chromdict['exclude'])]
                for j in range(5):
                    vsheet.write(vrows,j,row[j])
                vrows+=1
                chromcomp=allchromcompare(chromdict)
                allchromsheet.col(0).width=8400
                allchromsheet.write(allchromrows,0,i)
                for row in range(len(chromcomp)):
                    for col in range(len(chromcomp[row])):
                        val=chromcomp[row][col]
                        if type(val)==numpy.float64:
                            #print val
                            if val>0.05:
                                allchromsheet.write(allchromrows+row,1+col,val)
                            elif val>0.01:
                                allchromsheet.write(allchromrows+row,1+col,val,tan)
                            elif val>0.005:
                                allchromsheet.write(allchromrows+row,1+col,val,gold)
                            elif val>0.001:
                                allchromsheet.write(allchromrows+row,1+col,val,lightorange)
                            else:
                                allchromsheet.write(allchromrows+row,1+col,val,orange)
                        else:
                            allchromsheet.write(allchromrows+row,1+col,val)
                #writesheet(allchromsheet,chromcomp,allchromrows,1)
                allchromrows+=18
    
    writebook.save(os.path.join(folder,'Whites.xls'))
            
    

    
executechromvfiles(r'I:\Statistical analysis for Stacey (SHE6-01 thru 05)\SHE6-09 Excel files for statistical analysis WCs')
"""Revisions 7/15/13-
Remove URA locus from chrom 5-DONE
Mirror chromosome chart, add row 16- add mean at end of chromosome- DONE
Add formatting if statistically signficant- tan, gold, light orange, orange .05, .01, .005, .001"""