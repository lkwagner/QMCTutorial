from __future__ import print_function
import gen_hchain
import numpy as np
import json
import os

def runqwalk(filename):
  os.system("sub_qwalk %s 1 | qsub"%filename)


#################################
def write_jastrow(f):
  f.write("""JASTROW2 

GROUP { 
EEBASIS { 
EE
 CUTOFF_CUSP
 GAMMA 24.0
 CUSP 1.0
 CUTOFF 4.5
}
EEBASIS { 
EE
 CUTOFF_CUSP
 GAMMA 24.0
 CUSP 1.0
 CUTOFF 4.5
}
TWOBODY_SPIN { 
  FREEZE 
  LIKE_COEFFICIENTS { 0.25  0.0 } 
  UNLIKE_COEFFICIENTS { 0.0 0.5 } 
 }
} 
GROUP { 
EIBASIS { 
H
 POLYPADE
 BETA0 0.2
 NFUNC 4
 RCUT 4.5
}
ONEBODY { 
  COEFFICIENTS { H   0.0   0.0  0. 0. } 
 } 
EEBASIS { 
EE
 POLYPADE
 BETA0 0.5
 NFUNC 4
 RCUT 4.5
}
TWOBODY { 
  COEFFICIENTS {  0.0 0. 0. 0. }
 } 
} 
""")
#################################

def run_hf(basename,n,a):
  cg=gen_hchain.ChainGen(n,a)
  cg.write(basename)
  common="""method { VMC nstep 200 
  average { region_fluctuation maxn 4 } 
} 
include %s.sys\n \n"""%basename

  f=open(basename+"_afm.hf",'w')
  f.write(common+
          "trialfunc { include %s_afm.slater } \n "%basename)
  f.close()
  runqwalk(basename+"_afm.hf")

  f=open(basename+"_tb.hf",'w')
  f.write(common+
"trialfunc { include %s_tb.slater }"%basename)
  f.close()
  runqwalk(basename+"_tb.hf")

#################################

def run_variance(basename,n,a):
  cg=gen_hchain.ChainGen(n,a)
  cg.write(basename)
  write_jastrow(open("jastrow.in",'w'))
  common="""method { optimize }
  method { optimize } 
method { VMC nstep 200 
  average { region_fluctuation maxn 4 } 
} 
include %s.sys\n\n"""%basename

  f=open(basename+"_afm.opt",'w')
  f.write(common+
          """trialfunc { slater-jastrow
wf1 { include %s_afm.slater } 
wf2 { include jastrow.in } 
}"""%basename)
  f.close()
  runqwalk(basename+"_afm.opt")

  f=open(basename+"_tb.opt",'w')
  f.write(common+
          """trialfunc { slater-jastrow
wf1 { include %s_tb.slater } 
wf2 { include jastrow.in } 
}"""%basename)
  f.close()
  runqwalk(basename+"_tb.opt")

#################################


def run_dmc(basename,n,a):
  cg=gen_hchain.ChainGen(n,a)
  cg.write(basename)
  common="""method { DMC timestep 0.05 nblock 15 
  average { region_fluctuation maxn 4 } 
} 
include %s.sys\n\n"""%basename

  f=open(basename+"_afm.dmc",'w')
  f.write(common+
          """trialfunc { include %s_afm.opt.wfout } 
"""%basename)
  f.close()
  runqwalk(basename+"_afm.dmc")

  f=open(basename+"_tb.dmc",'w')
  f.write(common+
          """trialfunc { include %s_tb.opt.wfout }
"""%basename)
  f.close()
  runqwalk(basename+"_tb.dmc")

