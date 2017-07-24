#!/bin/bash

{partition_qos}
#SBATCH --nodes={nodes}
#SBATCH --job-name=maps_{tag}
#SBATCH --export=NONE
#SBATCH --output=logs/maps_{tag}_%j.out
#SBATCH --error=logs/maps_{tag}_%j.out
#SBATCH --mail-type=END,FAIL      # notifications for job done & fail
#SBATCH --license=SCRATCH
#SBATCH --license=project

ulimit -c 0

export OMP_NUM_THREADS=4
let ntasktot=24*{nodes}/$OMP_NUM_THREADS

#export PYTHONPATH=
export PYTHONNOUSERSITE=1

echo "PATH:" $PATH
module use /global/common/edison/contrib/hpcosmo/modulefiles
module unload altd
module use /global/common/edison/contrib/hpcosmo/modulefiles
module load toast-deps/20170427-gcc
export LD_LIBRARY_PATH=/global/common/edison/contrib/hpcosmo/toast-deps/20170427-gcc_conda/lib:$LD_LIBRARY_PATH
export PREFIX=/scratch3/scratchdirs/keskital/software
export PYTHONPATH=$PREFIX/lib/python3.5/site-packages:$PYTHONPATH
export PATH=$PREFIX/bin:$PATH
export PATH=/project/projectdirs/planck/software/keskital/edison/fits_tools:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$PREFIX/lib64:$LD_LIBRARY_PATH
export CFLAGS="-L$PREFIX/include"
export CXXFLAGS="-L$PREFIX/include"
export LDFLAGS="-L$PREFIX/lib"

module list

python=`which python3`
#echo $python
#echo $PYTHONPATH
bin=$PREFIX/bin

srun -n $ntasktot  --ntasks-per-node=6 --ntasks-per-socket=3 --cpus-per-task=4 --export=ALL $python -s $bin/toast_planck_sim.py @temp/maps_{tag}.par
