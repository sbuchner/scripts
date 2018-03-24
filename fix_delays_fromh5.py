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
parser.add_argument('-c', '--cable',dest='cable',action='store_true')
parser.add_argument('-a','--add',dest='add',metavar='add',type=float,help='additional delay')
#parser.add_argument('-u', '--update', dest='update', action='store_true', help='update files')   # by default existing files are not overwritten
#parser.add_argument('files', nargs='*')
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

            result.setdefault(d['name'], []).append((float(d['delay'])))
                                                  
        return result


print args.output
print args.tim
print args.delay



result=readDelaysFile(args.delay)
add=np.double(args.add)
print "%.2lg" %(add)
toa=open(args.tim,'r')
#toa=open('/home/sbuchner/MeerKAT/1909-investigate/J1909-3744.mk.tot.tim','r')
toa.readline()
new=open(args.output,'w')
new.write('FORMAT 1\n')

print result
for line in toa:
    
    
    a=line.split(' ')[:3]
    b=line.split(' ')[3:]
    fl=" ".join(b).replace('\n','')
    
    file=a[0]
    freq=a[1]
    ext=file.split('.')[-1]

    name=file.replace('.'+ext,'')

    mjd=np.double(a[2])
    print mjd
    try:
         
	delay=np.double(result[name][0])
	print "delay = %f" %(delay)
	if (args.add > 0.0):
		print "delaytot"
		delay = delay-add
		print delay
	print "tot",delay
	delay_mjd=np.double(delay*1E-9/(24*3600))
	print delay_mjd
	print "delay = %.2f nsec %.12f %.12f days" %(delay,mjd-delay_mjd,mjd)
        new.write("%s %s %.20lgi %s \n" %(file,freq,mjd-delay_mjd,fl))
#        new1.write("%s %s %.20lg %s -nant %d\n" %(file,freq,mjd-delay+delay1,fl,nant))

    except:
#        new.write("#%s %s\n" %(a,b))
#        new1.write("#%s %s\n" %(a,b))
      #  print "---%s" %(a)
        print "error"
	continue
    
new.close()
