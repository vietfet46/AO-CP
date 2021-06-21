#load libraries for CST
import os
import sys
sys.path.append(r"C:\Program Files (x86)\CST STUDIO SUITE 2020\AMD64\python_cst_libraries")
import cst
import cst.interface
from cst.interface import Project
import cst.results
# load libraries for optimization
import numpy as np
from scipy.optimize import minimize
#define fitness function
def cst_fun(x):
# I want to use Nelder-Mead algorithm for optimization. However, it doesn’t have bounds in #SciPy. So, I define the bounds by myself although it is a bad idea.
  if 30.0<=x[0]<=70.0 and 20.0<=x[1]<=35.0:
     mycst = cst.interface.DesignEnvironment() #open CST
     mycst1=cst.interface.DesignEnvironment.open_project(mycst, r"...\CST-Python\PhasedArray_1_theta=0.cst") #open CST project, that will be optimized at 0deg.
     #make VBA script to parameters change and project update
     par_change = 'Sub Main () \nStoreParameter("dl", '+str(x[0])+')\nStoreParameter("h",'+str(x[1])+')\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'
     mycst1.schematic.execute_vba_code(par_change, timeout=None) #execute VBA script
     cst.interface.DesignEnvironment.in_quiet_mode = True
     mycst1.modeler.run_solver() #run simulation
     cst.interface.DesignEnvironment.close(mycst) #close CST
     #get S11
     project = cst.results.ProjectFile(r"...\CST-Python\PhasedArray_1_theta=0.cst")
     S11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
     res=np.array(S11.get_ydata())
     #find max of S11
     opt_value1 = max(abs(res))
     #repeat for the project, that will be optimized at 45deg.
     mycst = cst.interface.DesignEnvironment()
     mycst1=cst.interface.DesignEnvironment.open_project(mycst, r"...\CST-Python\PhasedArray_1_theta=45.cst")
     mycst1.schematic.execute_vba_code(par_change,timeout=None)
     cst.interface.DesignEnvironment.in_quiet_mode = True
     mycst1.modeler.run_solver()
     cst.interface.DesignEnvironment.close(mycst)
     project = cst.results.ProjectFile(r"...\CST-Python\PhasedArray_1_theta=45.cst")
     S11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
     res=np.array(S11.get_ydata())
     opt_value2 = max(abs(res))
     #I want to get minimum S11 at 0deg and 45deg, so I have to find max and then minimize it
     print(str(opt_value1+opt_value2))
     return opt_value1+opt_value2
#if we out of bounds
  else:
     return 1.0
#set initial values of dl and h
x0 = np.array([35.0, 30.0])
#find minimum of the fitness function
res = minimize(cst_fun, x0, method='nelder-mead', options={'xatol': 1e-8, 'disp': True})
