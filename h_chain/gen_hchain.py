from __future__ import print_function
import numpy as np

class ChainGen:
  def __init__(self,n,a):
    self.n=n
    self.a=a
###############################################

  def write(self,basename):
    self.write_sys(open(basename+".sys",'w'))
    self.write_basis(open(basename+".basis",'w'))
    self.write_afm_orb(open(basename+"_afm.orb",'w'))
    self.write_afm_slater(basename+".basis",
                          basename+"_afm.orb",
                          open(basename+"_afm.slater",'w'))
    
    self.write_tb_orb(open(basename+"_tb.orb",'w'))
    self.write_tb_slater(basename+".basis",
                          basename+"_tb.orb",
                          open(basename+"_tb.slater",'w'))
    
    
###############################################
  def write_sys(self,f):
    f.write("SYSTEM { PERIODIC \n")
    if self.n%2 != 0:
      print("n must be even")
      quit()
    nspin=self.n/2
    f.write("NSPIN { %i %i } \n"%(nspin,nspin))
    for i in range(0,self.n):
      f.write("ATOM { H 1.0 COOR 0. 0. %g } \n"%(i*self.a))
    f.write("CUTOFF_DIVIDER 2.0 \n")
    f.write("""LATTICEVEC { 20.0 0. 0. 
       0. 20.0 0.
       0. 0.  %g } \n"""%(self.n*self.a) )
    f.write("}\n")
    f.write("""
PSEUDO { 
  H
  AIP 6 
  BASIS { H
   RGAUSSIAN 
   OLDQMC { 
0.0 1
3  
    1  4.4769199999999997885424818377942  1
    3  2.9763600000000001166711172118085  4.4769199999999997885424818377942
    2  3.0184199999999998809130374866072  -4.3211199999999996279598235560115
   }
  }
}
""")    
###############################################

  def write_basis(self,f):
    f.write("""BASIS { 
H
AOSPLINE
cusp -1

  GAMESS { 
S   6
               1         6.3592       0.003784
               2        3.54664       0.022388
               3        1.49344       0.091414
               4       0.551948        0.14998
               5       0.207203       0.375784
               6       0.079234      -0.098638
  }
}
""")
###############################################
  def write_afm_orb(self,f):
    for i in range(0,self.n):
      f.write("%i 1 %i 1\n"%(i+1,i+1))
    f.write("COEFFICIENTS\n 1.0 \n")

###############################################
  def write_afm_slater(self,basisname,orbname,f):
    f.write("SLATER\n")
    f.write("""ORBITALS { 
    CUTOFF_MO
    ORBFILE %s 
    NMO %i
    include %s
    CENTERS { USEGLOBAL } 
}\n"""%(orbname,self.n,basisname))
    f.write("DETWT { 1.0 } \n")
    f.write("STATES { \n    ")
    for i in range(0,self.n,2):
      f.write(" %i "%(i+1))
    f.write("\n    ")
    for i in range(1,self.n,2):
      f.write(" %i "%(i+1))
    f.write("}\n")
###############################################
  def write_tb_orb(self,f):
    T=np.zeros((self.n,self.n))
    for i in range(1,self.n-1):
      T[i,i+1]=-1
      T[i,i-1]=-1
    T[0,-1]=-1
    T[-1,0]=-1
    T[0,1]=-1
    T[-1,-2]=-1
    w,v=np.linalg.eig(T)
    eigenvecs=[]
    for i in range(0,self.n):
      eigenvecs.append((w[i],v[:,i]))
    eigenvecs.sort(key=lambda a: a[0])
    for e in eigenvecs:
      print(e)
    count=1
    for i in range(0,self.n):
      for j in range(0,self.n):
        f.write("%i 1 %i %i\n"%(i+1,j+1,count))
        count+=1
    f.write("COEFFICIENTS\n")
    count=1
    for e in eigenvecs:
      for d in e[1]:
        f.write(" %g "%d)
        if count%5==0:
          f.write("\n")
        count+=1
    f.write("\n")
###############################################
  def write_tb_slater(self,basisname,orbname,f):
    f.write("SLATER\n")
    f.write("""ORBITALS { 
    CUTOFF_MO
    ORBFILE %s 
    NMO %i
    include %s
    CENTERS { USEGLOBAL } 
}\n"""%(orbname,self.n,basisname))
    f.write("DETWT { 1.0 } \n")
    f.write("STATES { \n    ")
    norb=int(self.n/2)
    for i in range(0,norb):
      f.write(" %i "%(i+1))
    f.write("\n    ")
    for i in range(0,norb):
      f.write(" %i "%(i+1))
    f.write("}\n")



    
###############################################


if __name__ == "__main__":
  cg=ChainGen(6,3.0)
  cg.write("h_chain")

