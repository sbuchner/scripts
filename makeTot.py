#!/usr/bin/env python

import numpy as np
import os, sys, glob
import argparse
import psrchive
import subprocess
##################################################
# initialize parameters
parser = argparse.ArgumentParser(description='psradd .ar sub-ints to creates .tot file for observation, \
                                 scrunches the total file in pol,time and freq.')
#    parser.add_argument('-i', '--indir', dest='input_dir', metavar='<input_dir>', default='', help='specify input directory')
#    parser.add_argument('-o', '--outdir', dest='output_dir', metavar='<output_dir>', default='', help='specify output directory')
#    parser.add_argument('-e', '--eph', dest='ephem_file', metavar='<ephem_file>', default='', help='use ephemeris file to update archives')
#    parser.add_argument('-n', '--ntscr', dest='tscr_nsub', metavar='<ntscr>', nargs=1, help='dedisperse, time scrunch to n-subints and write out to file')
#    parser.add_argument('-t', '--tscr', dest='tscr', action='store_true', help='dedisperse, time scrunch and write out to file')
#    parser.add_argument('-f', '--fscr', dest='fscr', action='store_true', help='dedisperse, frequency scrunch and write out to file')
#    parser.add_argument('-c', '--clean', dest='clean_rfi', action='store_true', help='clean data from RFI using CoastGuard\'s cleaners')
#    parser.add_argument('-m', '--mask', dest='rfi_mask', nargs='?', const=True, default=None, help='apply RFI mask from file or use default one')
#    parser.add_argument('-p', '--psrsh', dest='psrsh_save', action='store_true', help='write zap commands to psrsh script file')

parser.add_argument('-i','--input',dest='input',metavar='<input_dir>',default='',help='input directory')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='verbose mode')
parser.add_argument('-o','--output',dest='output',metavar='output_dir',default='.',help='output directory')
parser.add_argument('-p','--psr',dest='psr',help='select this pulsar')
parser.add_argument('-u','--update',dest='update',action='store_true',help='update files')
args = parser.parse_args()

# median zap
##################################################
# start of code
# get current working directory
#cwd = os.getcwd()
cwd = '/data2/'
# define PTUSE archive directory
#arc = '/archive2/data/beamformer/pulsartiming/'

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

# Find all directories in the archive that have the pulsar obs
#direcs =glob.glob(str(arc) + 'PTUSE_1_*' + str(args.psr))
print args.input
if args.psr:
	puls=args.psr.replace('-','m').replace('+','p')
        print puls
        direcs=glob.glob(str(args.input)+'*'+puls+'*')
else:
	direcs=glob.glob(str(args.input)+'*')
#print direcs
# Add the subints 
for obs in direcs:
    print obs
    input_files = []
    input_dir = obs + '/'
    for file in os.listdir(input_dir):
        if file.endswith('.ar'):
            input_files.append(file)
    input_files.sort()
#    print input_files

    archive =psrchive.Archive_load(input_dir + input_files[0])

    psr=archive.get_source()
    print args.output+'/'+psr
    
    if os.access(args.output+'/'+psr, os.F_OK):
       print "exists"
    else:
       os.mkdir(args.output+'/'+psr)
    
    output_dir=args.output+'/'+psr	


    filename=archive.get_filename().split('/')[-1]
   
    print "First file = %s" %(filename)
    utc=filename.replace('-','',2).replace(':','',1).replace('-','T').split(':')[0]
    outputfile=output_dir+'/'+psr+'.'+utc+'.tot'
    print "Writing to %s" %(outputfile)
    print args.update
    e = os.access(outputfile,os.F_OK)
    print e
    if (os.access(outputfile, os.F_OK) and (not args.update)):
           print "Output file %s exists" %(outputfile)
           print "skipping %s" %(outputfile)
    else:    
           if args.verbose:
              print '\nLoading files from %s:' %(input_dir)
              print "writing" + outputfile
              
              subprocess.call(['psradd','-v', '--autoT','-o' + outputfile, obs + '/*.ar'])




