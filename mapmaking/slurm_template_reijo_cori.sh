#!/bin/bash

{partition_qos}
#SBATCH --nodes={nodes}
#SBATCH --job-name=maps_{tag}
#SBATCH --export=ALL
#SBATCH --output=logs/maps_{tag}_%j.out
#SBATCH --error=logs/maps_{tag}_%j.out
#SBATCH --mail-type=END,FAIL      # notifications for job done & fail
#SBATCH -C haswell
#SBATCH --license=SCRATCH
#SBATCH --license=project

ulimit -c 0

export OMP_NUM_THREADS=4
let ntasktot=24*{nodes}/$OMP_NUM_THREADS

#export PYTHONPATH=
export PYTHONNOUSERSITE=1

module list

python=`which python3`
#echo $python
#echo $PYTHONPATH
bin=$PREFIX/bin

srun -n $ntasktot  --ntasks-per-node=6 --ntasks-per-socket=3 --cpus-per-task=4 --export=ALL $python -s $bin/toast_planck_sim.py @temp/maps_{tag}.par
