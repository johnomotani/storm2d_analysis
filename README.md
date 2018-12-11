Analysing STORM2D filament simulations
--------------------------------------

1. Download (or clone) STORM from github
   ```
   git clone https://github.com/boutproject/STORM.git
   ```

1. Compile storm2d:
   ```
   cd STORM/storm2d
   cp make.config.example make.config
   nano make.config
   make
   ```
   Editing the path in make.config to point to your copy of BOUT++.
   Use BOUT++ v4.2 (currently the master branch).

1. Download the files from this repo

1. Copy BOUT.inp.2filaments to STORM/storm2d/data/BOUT.inp

1. Copy either/both the storm2d_analysis.ipynb notebook or storm2d_analysis.py
   script to STORM/storm2d/data

1. Run the simulation, e.g. in the storm2d directory
   ```
   mpirun -np 4 ./storm2d
   ```

1. Install jupyter if necessary
   ```
   pip3 install --user jupyter
   export PATH=~/.local/bin:$PATH
   ```

1. Open and run the Jupyter notebook
   ```
   jupyter notebook
   ```
   and click on `storm2d_analysis.ipynb`

1. Experiment with different options by changing the BOUT.inp file
   1. filament properties in [blob] and [blob2] sections
   1. simulation parameters in [storm] section

   You will find brief descriptions of most of the options in
   `STORM/doc/options.md`  
   https://github.com/boutproject/STORM/blob/master/doc/options.md
