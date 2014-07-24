# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 21:13:04 2012

@author: Beth Cimini
"""

from uncertainties import ufloat
from uncertainties.umath import *
import xlrd
import csv

def domyworkforme(filename,outfilename,onsheet,offsheet):
    book=xlrd.open_workbook(filename,on_demand=True)
    on=book.sheet_by_name(onsheet)
    off=book.sheet_by_name(offsheet)
    writer=csv.writer(open(outfilename,'wb'))
    headings=on.row_values(0)
    for i in range(len(headings)):
        if 'Normalized mean' in headings[i]:
            meancol=i
        if 'Normalized st.dev.' in headings[i]:
            stdevcol=i
        if 'Mean per frame intensity-Red' in headings[i]:
            redmeancol=i
        if 'Mean per frame intensity-Green' in headings[i]:
            greenmeancol=i
        if 'St.dev. per frame intensity-Red' in headings[i]:
            redstdevcol=i
        if 'St.dev. per frame intensity-Green' in headings[i]:
            greenstdevcol=i    
    divlist=[]
    i=1
    writer.writerow(['New mean','New stdev','','Old mean', 'Old stdev'])
    while on.cell(i,meancol).value!='':
        onint=ufloat((on.cell(i,meancol).value,on.cell(i,stdevcol).value))
        offint=ufloat((off.cell(i,meancol).value,off.cell(i,stdevcol).value))
        redoffint=ufloat((off.cell(i,redmeancol).value,off.cell(i,redstdevcol).value))
        greenoffint=ufloat((off.cell(i,greenmeancol).value,off.cell(i,greenstdevcol).value))
        redonint=ufloat((on.cell(i,redmeancol).value,on.cell(i,redstdevcol).value))
        greenonint=ufloat((on.cell(i,greenmeancol).value,on.cell(i,greenstdevcol).value))
        try:
            div=onint/offint
            print div
            divlist.append(div)
            olddiv=((greenonint/greenoffint)/(redonint/redoffint))
            writer.writerow([div.nominal_value,div.std_dev(),'',olddiv.nominal_value,olddiv.std_dev()])
        except:
            divlist.append(0)
            writer.writerow([0,0,'',0,0])
        i+=1
    print divlist
    
domyworkforme(r'F:\combined20120511_19\2012051119.xls',r'F:\combined20120511_19\ctl.csv',r'ctlonConvertedFoci',r'ctloffConvertedFoci')