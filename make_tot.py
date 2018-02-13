#!/usr/bin/env python

# Copyright (C) 2017 by Sarah Buchner
# Licensed under the Academic Free License version 3.0
# This program comes with ABSOLUTELY NO WARRANTY.
# You are free to modify and redistribute this code as long
# as you do not remove the above attribution and reasonably
# inform recipients that you have modified the original work.

import numpy as np
import os, sys, glob
import argparse
import psrchive
import subprocess

# initialize parameters
parser = argparse.ArgumentParser(description='psradd .ar sub-ints to creates .tot file for observation') 
                                 
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='verbose mode')
parser.add_argument('-o','--output',dest='output',metavar='output_dir',default='.',help='output directory')
parser.add_argument('-p','--psr',dest='psr',help='select this pulsar')
parser.add_argument('-u','--update',dest='update',action='store_true',help='update files')   # by default existing files are not overwritten
parser.add_argument('files', nargs='*') 
args = parser.parse_args()

#check that we have write permission in output dir
if not args.output:
    print '\nOption --outdir not specified. Selecting current directory.\n'
    output_dir = cwd
else:
    if os.access(args.output, os.F_OK):
        output_dir = args.output
    else:
        raise RuntimeError('Output directory does not exist.')
    if os.access(args.output, os.W_OK) and os.access(args.output, os.X_OK) and os.access(args.output, os.R_OK):
        pass
    else:
        raise RuntimeError('Output directory without write permissions.')
if args.psr:
    puls=args.psr.replace('-','m').replace('+','p')
    print "Processing pulsar %s"  %(args.psr)
 
for obs in args.files:
# if psr selected then process only that pulsar    
    if args.psr:
        if puls not in obs:
		if args.verbose:
			print "Skipping obs %s" %(obs)
		continue
#
    print obs
#
    input_files = []
    input_dir = obs + '/'
    for file in os.listdir(input_dir):
        if file.endswith('.ar'):
            input_files.append(file)
    input_files.sort()
#    print input_files
    if len(input_files)<1:
	print "skipping %s" %(obs)
	continue
    archive =psrchive.Archive_load(input_dir + input_files[0])

    psr=archive.get_source()
    
    if not os.access(args.output+'/'+psr, os.F_OK):
       os.mkdir(args.output+'/'+psr)
    
    output_dir=args.output+'/'+psr	


    filename=archive.get_filename().split('/')[-1]
   
    utc=filename.replace('-','',2).replace(':','',2).replace('-','T').replace('.ar','')
    print utc
    outputfile=output_dir+'/'+psr+'.'+utc+'.tot'
    e = os.access(outputfile,os.F_OK)
    if (os.access(outputfile, os.F_OK) and (not args.update)):
           print "Output file %s exists skipping" %(outputfile)

    else:  
           print '\nLoading files from %s -> %s\n' %(input_dir,outputfile)
  
           if args.verbose:
              subprocess.call(['psradd','-v', '--autoT','-o' + outputfile, obs + '/*.ar'])
	   else:
              subprocess.call(['psradd', '--autoT','-o' + outputfile, obs + '/*.ar'])
	



