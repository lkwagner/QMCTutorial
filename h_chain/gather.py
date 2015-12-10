import read_numberfluct
import copy
import os
import glob
import yaml
import numpy as np
import math


def get_qwalk_en(filename):
  enline=""
  for line in open(filename, 'r'):
    if 'total_energy0' in line:
      enline=line
      break
  spl=enline.split()
  if len(spl) > 0:
    return (float(spl[1]),float(spl[3]))
  else: 
    return None

method_translate={'hf':'vmc','opt':'vmc','dmc':'dmc'}
twf_translate={'hf':'','opt':'-j','dmc':'-j'}


nvals=[10,16]
avals=[1.0,1.5,2.0,3.0,4.0]
data=[]
for n in nvals:
  for a in avals:
    basename="h"+str(n)+str(a)
    entry={}
    entry['a']=a
    entry['basename']=basename
    entry['n']=n
    for twf in ['afm','tb']:
      for ext in ['hf','opt','dmc']:
        entry['twf']=twf+twf_translate[ext]
        entry['ext']=ext
        entry['method']=method_translate[ext]
        fname=basename+'_'+twf+"."+ext
        outfile="scratch/"+fname+".o"
        print(outfile)
        if os.path.isfile(outfile):
          en=get_qwalk_en(outfile)
          entry['en']=en[0]
          entry['en_err']=en[1]
          #this returns the probability distribution p(n_isigma,n_jsigma')
          number=read_numberfluct.read_number_dens(open(outfile))
          if number[0] != None:
            avg,var,cov,avg_err,var_err,cov_err=read_numberfluct.moments(number[0],number[1])
            entry['variance']=float(var[0,0]+var[1,0])
            entry['variance_err']=float(math.sqrt(var_err[0,0]**2+var_err[1,0]**2))
            entry['double_occupancy']=float(number[0][0,1,0,0,1,1])
            entry['double_occupancy_err']=float(number[1][0,1,0,0,1,1])

          #this returns the avg,var,covar,avg_err, var_err, and covar_err
          #entry['moments']=read_numberfluct.moments(entry['number'][0],entry['number'][1])
          if entry['en'] != None and number[0]!=None:
            data.append(copy.deepcopy(entry))
         
        

yaml.dump(data,open("results.yaml",'w'))
