# bk_scripts
Repository of bash/python/whatever scripts/tools I use. Should be able to clone, add to bin to PATH and use.

`./setup.sh` is convenience for quickly adding to .bashrc/.profile/.bash_profile

- `bk_clean` is a python script for parsing program outputs and outputing .csv format. Can take Horovod and OSU-Microbenchmark files as inputs. 
- `mdpdfdt` is a shell script that wraps pandoc. Takes a markdonwn file as input and exports it to the destop as a pdf
- `chk` is for checking SLURM job status on ComputeCanada clusters. Calling `chk <cluster_name>` will make an squeue call over ssh and compare it to the preveous call to chk.
