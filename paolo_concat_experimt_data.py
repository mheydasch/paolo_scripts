#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:42:45 2019

@author: max
"""

import pandas as pd
import sys
import os
import re
import argparse
def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)

  args = parser.parse_args()
  return(args)
#%%  
filesep=os.sep
path='/Volumes/imaging.data/Paolo/MCF10A_TimeLapse/'
#%%
def find_csv(path):
    exclude=['cp.out']
    findfile='experimentDescription.csv'
    filelist=[]
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        if findfile in files:
            filepath=os.path.join(root, findfile)
            filelist.append(filepath)
    return filelist


datepattern=re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
def concat_csv(path):
    filelist=find_csv(path)
    csvlist=[]
    for file in filelist:
        temp=pd.read_csv(file, sep=';')
        splitpath=file.split(filesep)
        for i in splitpath:
            if re.search(datepattern, i)!=None:
                temp['experiment']=i
                break
        csvlist.append(temp)
    fullcsv=pd.concat(csvlist)
    pd.to_csv(os.path.join(path, 'concat_experiment_description.csv'))
    return fullcsv


#%%            
if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    concat_csv(path)
    print(args)            