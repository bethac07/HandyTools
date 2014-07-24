from pyPdf import PdfFileReader, PdfFileWriter
import xlrd, xlwt
from xlutils.copy import copy
import os

def processoligofiles(directory='G:\Blackburn Lab\Oligonucleotides'):
    listoffiles=os.listdir(directory)
    for i in listoffiles:
        if 'Spec' in i:
            if '.pdf' in i:
                cc=os.path.join(directory,i)
                a=open(cc,'rb')
                input1=PdfFileReader(a)
                b=input1.getPage(0)
                c=b.extractText()

                sind=c.index('Sequence')
                EHBnum=c[sind+9:sind+14]
                d='nmoleDNAoligo'
                if d not in c:
                    d='nmoleDNAOligo'
                if c[sind+14]=='-':
                    if c[c.index(d)-1]=='5':
                        ident=c[sind+15:c.index(d)-2]
                    elif c[c.index(d)-1]=='0':
                        ident=c[sind+15:c.index(d)-3]
                if c[sind+14]!='-':
                    if c[c.index(d)-1]=='5':
                        ident=c[sind+14:c.index(d)-2]
                    elif c[c.index(d)-1]=='0':
                        ident=c[sind+14:c.index(d)-3]                
                fileout=PdfFileWriter()
                for i in range(input1.numPages):
                    fileout.addPage(input1.getPage(i))
                outfilename=os.path.join(directory,(EHBnum+'- '+ident+'.pdf'))
                output=file(outfilename,'wb')
                fileout.write(output)
                a.close()
                output.close()
                os.remove(cc)
        
def sendoligofiles(directory='G:\Blackburn Lab\Oligonucleotides',excel='G:\Blackburn Lab\Oligonucleotides\Oligos.xls'):
    listoffiles=os.listdir(directory)
    excelfile=xlrd.open_workbook(excel)
    excelsheet=excelfile.sheet_by_index(0)
    writablexl=copy(excelfile)
    writesheet=writablexl.get_sheet(0)
    numberdone=int(excelsheet.cell(excelsheet.nrows-1,1).value[4:])+1
    sheetlength=excelsheet.nrows
    done=False
    while done==False:
        thisnum=False
        number=numberdone
        for i in listoffiles:
            if str(number) in i:
                if '.pdf' in i:
                    cc=os.path.join(directory,i)
                    a=open(cc,'rb')
                    input1=PdfFileReader(a)
                    b=input1.getPage(0)
                    c=b.extractText()
                    #Want EHB code, name, sequence, date
                    sind=c.index('Sequence')
                    EHBnum=c[sind+9:sind+14]
                    d='nmoleDNAoligo'
                    if d not in c:
                        d='nmoleDNAOligo'
                    if c[sind+14]=='-':
                        if c[c.index(d)-1]=='5':
                            ident=c[sind+15:c.index(d)-2]
                        elif c[c.index(d)-1]=='0':
                            ident=c[sind+15:c.index(d)-3]
                    if c[sind+14]!='-':
                        if c[c.index(d)-1]=='5':
                            ident=c[sind+14:c.index(d)-2]
                        elif c[c.index(d)-1]=='0':
                            ident=c[sind+14:c.index(d)-3] 
                    if 'Bases5-' in c:
                        cslice=c[c.index('Bases5-')+7:]
                        for j in cslice:
                            if j=='-':
                               endind=cslice.index(j)
                               pass
                        sequence=cslice[0:endind]
                    date=c[0:8]
        
                    writesheet.write(sheetlength,0,'Beth Cimini')
                    writesheet.write(sheetlength,1,'oEHB'+EHBnum)
                    writesheet.write(sheetlength,2,ident)
                    writesheet.write(sheetlength,3,sequence)
                    writesheet.write(sheetlength,4,date)
                    writesheet.write(sheetlength,5,'IDT')
                    
                    a.close()
                    thisnum=True
                    number+=1
                    sheetlength+=1
            if thisnum==False:
                done=True
                    
            
    writablexl.save(excel)
   
if __name__=='__main__':
    processoligofiles()
    sendoligofiles()
