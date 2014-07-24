# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:41:47 2013

@author: Beth Cimini
"""
import xlrd
import xlwt
from xlutils.copy import copy

def removethischaracter(filename,character):
    a=xlrd.open_workbook(filename)
    aa=a.sheet_by_index(0)
    b=copy(a)
    bb=b.get_sheet(0)
    for i in range(3,aa.nrows):
        cellval=str(aa.cell(i,1).value)
        if character in cellval:
            index=cellval.index(character)
            cellval=cellval[:index]+cellval[index+1:]
        bb.write(i,1,cellval)
    b.save(filename)
    
removethischaracter('C:/Users/Beth Cimini/Desktop/TR_HuGene10st.xls','.')