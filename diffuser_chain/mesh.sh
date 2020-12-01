#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 diffuser_main.py 

cd diffuser_design
sh config_control.sh

cd 0_diffuser_main
cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar -force
runParallel createPatch -overwrite

rm log.checkMesh
runParallel checkMesh

cd ..
cd ..
