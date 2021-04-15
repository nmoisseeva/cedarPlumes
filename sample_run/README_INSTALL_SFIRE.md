Installing WRF-SFIRE on Cedar
=============================

1. Download the code:
```
[~]$ wget https://github.com/openwfm/WRF-SFIRE/archive/fmoist-run-fix.tar.gz
```
2. Unpack the program:
```
[~]$ tar -xvf fmoist-run-fix.tar.gz
```
3. Load the modules:
```
[~]$  module load StdEnv/2020
[~]$  module load intel netcdf netcdf-fortran perl

[~]$ module list

Currently Loaded Modules:
  1) CCconfig                 4) StdEnv/2020    (S)   7) hdf5/1.10.6          (io)  10) ucx/1.8.0             13) expat/2.2.9 (t)
  2) gentoo/2020     (S)      5) gcccore/.9.3.0 (H)   8) netcdf/4.7.4         (io)  11) libfabric/1.10.1      14) perl/5.30.2 (t)
  3) imkl/2020.1.217 (math)   6) gcc/9.3.0      (t)   9) netcdf-fortran/4.5.2 (io)  12) openmpi/4.0.3    (m)
```
4. Set the environment variables and configure the program:
```
[~]$ cd WRF-SFIRE-fmoist-run-fix
[~]$ ls
arch  clean    configure  dyn_em   external  hydro  LICENSE.txt  Makefile  README     Registry  share  tools  wrftladj
chem  compile  doc        dyn_nmm  frame     inc    main         phys      README.md  run       test   var

export NETCDF=$EBROOTNETCDFMINFORTRAN
export NETCDF_classic=1
```
5. Run: ./configure

```
[~] ./configure

checking for perl5... no
checking for perl... found /cvmfs/soft.computecanada.ca/easybuild/software/2020/Core/perl/5.30.2/bin/perl (perl)
Will use NETCDF in dir: /cvmfs/soft.computecanada.ca/easybuild/software/2020/avx2/Compiler/gcc9/netcdf-fortran/4.5.2
HDF5 not set in environment. Will configure WRF for use without.
PHDF5 not set in environment. Will configure WRF for use without.
Will use 'time' to report timing information
$JASPERLIB or $JASPERINC not found in environment, configuring to build without grib2 I/O...
------------------------------------------------------------------------
Please select from among the following Linux x86_64 options:

  1. (serial)   2. (smpar)   3. (dmpar)   4. (dm+sm)   PGI (pgf90/gcc)
  5. (serial)   6. (smpar)   7. (dmpar)   8. (dm+sm)   PGI (pgf90/pgcc): SGI MPT
  9. (serial)  10. (smpar)  11. (dmpar)  12. (dm+sm)   PGI (pgf90/gcc): PGI accelerator
 13. (serial)  14. (smpar)  15. (dmpar)  16. (dm+sm)   INTEL (ifort/icc)
                                         17. (dm+sm)   INTEL (ifort/icc): Xeon Phi (MIC architecture)
 18. (serial)  19. (smpar)  20. (dmpar)  21. (dm+sm)   INTEL (ifort/icc): Xeon (SNB with AVX mods)
 22. (serial)  23. (smpar)  24. (dmpar)  25. (dm+sm)   INTEL (ifort/icc): SGI MPT
 26. (serial)  27. (smpar)  28. (dmpar)  29. (dm+sm)   INTEL (ifort/icc): IBM POE
 30. (serial)               31. (dmpar)                PATHSCALE (pathf90/pathcc)
 32. (serial)  33. (smpar)  34. (dmpar)  35. (dm+sm)   GNU (gfortran/gcc)
 36. (serial)  37. (smpar)  38. (dmpar)  39. (dm+sm)   IBM (xlf90_r/cc_r)
 40. (serial)  41. (smpar)  42. (dmpar)  43. (dm+sm)   PGI (ftn/gcc): Cray XC CLE
 44. (serial)  45. (smpar)  46. (dmpar)  47. (dm+sm)   CRAY CCE (ftn $(NOOMP)/cc): Cray XE and XC
 48. (serial)  49. (smpar)  50. (dmpar)  51. (dm+sm)   INTEL (ftn/icc): Cray XC
 52. (serial)  53. (smpar)  54. (dmpar)  55. (dm+sm)   PGI (pgf90/pgcc)
 56. (serial)  57. (smpar)  58. (dmpar)  59. (dm+sm)   PGI (pgf90/gcc): -f90=pgf90
 60. (serial)  61. (smpar)  62. (dmpar)  63. (dm+sm)   PGI (pgf90/pgcc): -f90=pgf90
 64. (serial)  65. (smpar)  66. (dmpar)  67. (dm+sm)   INTEL (ifort/icc): HSW/BDW
 68. (serial)  69. (smpar)  70. (dmpar)  71. (dm+sm)   INTEL (ifort/icc): KNL MIC
 72. (serial)  73. (smpar)  74. (dmpar)  75. (dm+sm)   FUJITSU (frtpx/fccpx): FX10/FX100 SPARC64 IXfx/Xlfx

Enter selection [1-75] : 15
------------------------------------------------------------------------
Compile for nesting? (1=basic, 2=preset moves, 3=vortex following) [default 1]: 1

Configuration successful!
...

```

6. The last step is to compile:
```
[~]$ ./compile -j 4 em_fire > compile.log 
```
Review the compile log to make sure there are no errors. Successful installation will produce an ideal.exe and wrf.exe files in ./main folder

