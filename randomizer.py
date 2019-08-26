"""A python script to rename files.  Needs Python 2 or 3, easygui, numpy,
and openpyxl
Beth Cimini, 2014-2019
"""

from openpyxl import Workbook
import os
import easygui as eg
from numpy import random

def file_name_randomizer():
    folder=eg.diropenbox('Where are the files you want to randomize?')
    files=os.listdir(folder)
    foldname=os.path.split(folder)[1]
    workbook=Workbook()
    name=foldname+" randomization"
    while len(name)>=31:
        name=eg.enterbox("Filename "+name+" is too long- enter a shorter one")
    randsheet = workbook.active
    randsheet.title = name
    rowcount=2
    numberlist=[]
    randsheet['A1'] = 'Code'
    randsheet['B1'] = 'OriginalName'
    for i in files:
        number="%0*d" %(6,random.randint(0,len(files)*3))
        while number in numberlist:
            number="%0*d" %(6,random.randint(0,len(files)*3))
        randsheet['A'+str(rowcount)] = number
        randsheet['B'+str(rowcount)] = i
        os.rename(os.path.join(folder,i),os.path.join(folder,number+'.tif'))
        rowcount+=1
        numberlist.append(number)
    workbook.save(filename = os.path.join(folder,name+'.xlsx'))

file_name_randomizer()
