This script uses numpy, matplotlib and PyQt4 for fast visualization of DX files produced by APBS or PMEpot from VMD.
Installation:
install numpy, matplotlib and PyQt4 to your distro
run app 
python dx_plotter.py

You may use this library for reading DX files to np.array:
from dx_plotter.py import open_dx
grid,scale,origin=open_dx('some_path_to_dx.dx')