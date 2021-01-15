# Installation instructions for WRF-SFIRE on Cedar

nmoisseeva@eoas.ubc.ca \
January 14, 2021 

This is a brief summary of how to install WRF-SFIRE LES on Cedar cluster.

### 1. Go to your projects directory
```bash
cd project/def-rstull/username/.
```
### 2. Clone current SFIRE GitHub repository.
```bash
git clone https://github.com/openwfm/WRF-SFIRE.git
```
### 3. Prepare compilers and set paths.
* ensure environmental variables are set correctly (see standard WRF documentation)
    - e.g. my current `.bashrc` file has the following two variables
    ```bash
    export WRFIO_NCD_LARGE_FILE_SUPPORT=1
    export NETCDF=/cvmfs/soft.computecanada.ca/easybuild/software/2017/avx2/Compiler/intel2019/netcdf-fortran/4.4.5/
    ``
* load required compiles 
    - e.g. my loaded modules incuded (output of `module list`)
```
Currently Loaded Modules:
  1) nixpkgs/16.09   (S)      3) gcccore/.5.4.0  (H)   5) ifort/.2016.4.258 (H)   7) openmpi/2.1.1 (m)
  2) imkl/11.3.4.258 (math)   4) icc/.2016.4.258 (H)   6) intel/2016.4      (t)   8) StdEnv/2016.4 (S)

  Where:
   S:     Module is Sticky, requires --force to unload or purge
   m:     MPI implementations / Implémentations MPI
   math:  Mathematical libraries / Bibliothèques mathématiques
   t:     Tools for development / Outils de développement
   H:                Hidden Module
```
    
