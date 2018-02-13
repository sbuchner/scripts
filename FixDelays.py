import csv
import numpy as np

def readDelaysFile(file):
    
    result={}
    with open(file,'r') as f:
        line=csv.DictReader(f)
        print line
        for d in line:
name;SB;target;NAnts;ants;delay;ref;HDel;VDel

                result.setdefault(d['name'],[]).append((float(d['delay']),float(d['HDel']),float(d['VDel']),int(d['nants'])))
    return result
                
