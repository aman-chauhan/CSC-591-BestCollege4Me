import re
import os
import sys
import json
import time
import math
import pandas as pd

def isInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def isFloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def main():
    rawpath="../raws/CollegeScorecard_Raw_Data"
    data={}
    global_attrs=None
    files=[f for f in os.listdir(rawpath) if (os.path.isfile(os.path.join(rawpath,f)) and not f.startswith('.'))]
    plen=50
    for file in sorted(files):
        attrs=None
        total=0
        total=len(open(os.path.join(rawpath,file)).readlines())
        print("\nAccessing file "+file+" with "+str(total)+" records.")
        with open(os.path.join(rawpath,file)) as fp:
            cnt=0
            for line in fp.readlines():
                if cnt==0:
                    global_attrs=line.strip().split(",")
                    attrs=line.strip().split(",")
                else:
                    row=line.strip().split(",")
                    id=int(row[0])
                    if id not in data:
                        data[id]={}
                    for i in range(len(attrs)):
                        if attrs[i] not in data[id]:
                            data[id][attrs[i]]=None
                        if row[i]=='NULL' or row[i]=='null':
                            data[id][attrs[i]]=None
                        elif isInt(row[i]):
                            data[id][attrs[i]]=int(row[i])
                        elif isFloat(row[i]):
                            data[id][attrs[i]]=float(row[i])
                        else:
                            data[id][attrs[i]]=row[i]
                cnt=cnt+1
                progress=math.floor((cnt/total)*plen)
                print("\r",end="")
                print("["+"#"*(progress)+" "*(plen-progress)+"]",end="")

    with open('../data/attributes.txt','w') as fp:
        s="\n".join(global_attrs)
        fp.write(s)

    print("\nWriting the data to disk...")
    with open('../data/combined.csv','w') as fp:
        s=",".join(global_attrs)
        fp.write(s+"\n")
        for id in sorted(data.keys()):
            row=[]
            for x in global_attrs:
                row.append(data[id][x])
            fp.write(str(row)[1:-1]+"\n")


if __name__=="__main__":
    main()
