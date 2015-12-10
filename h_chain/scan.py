from __future__ import print_function
import gen_hchain
import numpy as np
import json
import os

from gen_method import * 

#################################
tmpdir="scratch2"
if not os.path.isdir(tmpdir):
  os.mkdir(tmpdir)
os.chdir(tmpdir)


n=10
avals= [1.0,2.0,3.0,4.0,5.0]
for a in avals:
  basename="h"+str(n)+str(a)
  run_hf(basename,n,a)
  #run_variance(basename,n,a)
  #run_dmc(basename,n,a)
  

