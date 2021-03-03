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
```

6. Now, it is time to compile:
```
[~]$ ./compile

Usage:

   compile [-j n] wrf   compile wrf in run dir (NOTE: no real.exe, ndown.exe, or ideal.exe generated)

   or choose a test case (see README_test_cases for details) :
      compile [-j n] em_b_wave
      compile [-j n] em_convrad
      compile [-j n] em_esmf_exp
      compile [-j n] em_fire
      compile [-j n] em_grav2d_x
      compile [-j n] em_heldsuarez
      compile [-j n] em_hill2d_x
      compile [-j n] em_les
      compile [-j n] em_quarter_ss
      compile [-j n] em_real
      compile [-j n] em_scm_xy
      compile [-j n] em_seabreeze2d_x
      compile [-j n] em_squall2d_x
      compile [-j n] em_squall2d_y
      compile [-j n] em_tropical_cyclone
      compile [-j n] nmm_real
      compile [-j n] nmm_tropical_cyclone

  compile -j n               parallel make using n tasks if supported (default 2)
  compile -h                 help message
``
Compile using the command:
```
./compile -j 4 wrf 
```

