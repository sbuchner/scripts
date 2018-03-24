#!/usr/bin/env python

# Copyright (C) 2017 by Sarah Buchner
# Licensed under the Academic Free License version 3.0
# This program comes with ABSOLUTELY NO WARRANTY.
# You are free to modify and redistribute this code as long
# as you do not remove the above attribution and reasonably
# inform recipients that you have modified the original work.

import numpy as np
import os
import sys
import glob
import argparse
import subprocess
import csv

# initialize parameters
parser = argparse.ArgumentParser(description='psradd .ar sub-ints to creates .tot file for observation')

parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='verbose mode')
parser.add_argument('-o', '--output', dest='output', metavar='output_dir', default='.', help='output directory')
parser.add_argument('-t', '--tim', dest='tim')
parser.add_argument('-d', '--delay', dest='delay')
parser.add_argument('-c', '--cable',dest='cable',action='store_true',help='correct for cable length')
parser.add_argument('-a','--add',dest='add',metavar='add',type=float,help='additional delay')
args = parser.parse_args()
if args.cable:
	print "include cable"
if args.add:
	print "additional delay %.2f" %(args.add)

def readDelaysFile(file):

    result = {}
    with open(file, 'r') as f:
        line = csv.DictReader(f, delimiter=';')
        for d in line:

            result.setdefault(d['name'], []).append((float(d['delay']), float(d['HDel']), float(d['VDel']), int(d['NAnts'])))
                                                  
        return result


result=readDelaysFile(args.delay)
add=np.double(args.add)
toa=open(args.tim,'r')
toa.readline()
new=open(args.output,'w')
new.write('FORMAT 1\n')

for line in toa:
    
    a=line.split(' ')[:3]
    b=line.split(' ')[3:]
    fl=" ".join(b).replace('\n','')
    
    file=a[0]
    freq=a[1]
    ext=file.split('.')[-1]

    name=file.replace('.'+ext,'')

    mjd=np.double(a[2])
    try:
         
	max_delay=np.double(result[name][0][0])
        extra_delay=max_delay*1.01
        cable=np.double(result[name][0][1])/(3E8*0.7)*1E6
        print "max_delay %.2f %.2f" %(max_delay,cable)
	nant=int(result[name][0][3])
    
        delaytot = extra_delay
        if (args.cable):
                print "include cable %.2f" %(cable)

		delaytot = delaytot-cable
		print delaytot
	if (args.add > 0.0):
		print "delaytot"
		delaytot = delaytot-add
		print delaytot
	delaytot_mjd=np.double(delaytot*1E-6/(24*3600))
	print "delay = %.2f usec %.12f %.12f days" %(delaytot,mjd-delaytot_mjd,mjd)
        new.write("%s %s %.20lgi %s -nant %d \n" %(file,freq,mjd-delaytot_mjd,fl,nant))

    except:
        print "error on file" %(file)
	continue
    
new.close()
