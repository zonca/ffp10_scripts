#!/bin/bash

##SBATCH --partition=debug
#SBATCH --partition=regular
##SBATCH --qos=special_planck
#SBATCH --qos=premium
#SBATCH --nodes={nodes}
#SBATCH --time=00:24:00
#SBATCH --job-name=maps_{tag}
#SBATCH --export=ALL
#SBATCH --output=logs/slurm-%j.out
#SBATCH --error=logs/slurm-%j.out
#SBATCH --mail-type=END,FAIL      # notifications for job done & fail
#SBATCH --license=SCRATCH
#SBATCH --license=project

ulimit -c unlimited

export OMP_NUM_THREADS=4
let ntasktot=24*{nodes}/$OMP_NUM_THREADS

#export PYTHONPATH=
export PYTHONNOUSERSITE=1

echo "PATH:" $PATH
module use /global/common/edison/contrib/hpcosmo/modulefiles
module load toast-deps
export PREFIX=/global/project/projectdirs/planck/software/zonca/software/toast-prefix
export PYTHONPATH=$PREFIX/lib/python3.5/site-packages:$PYTHONPATH
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH

python=`which python3`
#echo $python
#echo $PYTHONPATH
bin=$PREFIX/bin

srun -n $ntasktot  --ntasks-per-node=6 --ntasks-per-socket=3 --cpus-per-task=4 --export=ALL $python -s $bin/toast_planck_sim.py @temp/maps_{tag}.par
