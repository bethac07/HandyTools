import easygui as eg
import os

def givenfile(fileinname,fileoutname):
    b=open(fileinname)
    d=b.readlines()
    c=[]
    y=[]
    for aa in d:
        if "SPOT " in aa:
            aa=aa[(aa.index("SPOT ")+5):-1]
            if ' ' in aa:
                z=aa.index(' ')
                aa=((aa[0:z]),(aa[z+1:]))
                c.append(aa)
        if "Time Point" in aa:
            if "#" not in aa:
                aa=(aa[aa.index(':')+2:-6])
                y.append(aa)

    m=open(fileoutname,'w')
    for i in y:
        m.write(i+',')

    m.write('\n')

    for i in c:
        m.write(str(i)+'\n')

    b.close()
    m.close()

def runwholefolder():
    direct=eg.diropenbox()
    for i in os.listdir(direct):
        if 'R3D.dv.log' in i:
            print i
            givenfile(os.path.join(direct,i),os.path.join(direct,i[:-7]+'simple.txt'))
            
if __name__=='__main__':
    runwholefolder()