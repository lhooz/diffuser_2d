#!/bin/bash --login
#$ -pe smp.pe 4
#$ -cwd
#$ -m bea
#$ -M hao.lee0019@yahoo.com

module load apps/binapps/anaconda3/2019.07  # Python 3.7.3
module load apps/binapps/paraview/5.7.0
module load apps/gcc/openfoam/v1906
source $foamDotFile

. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

sh mesh.sh
sh solver.sh
