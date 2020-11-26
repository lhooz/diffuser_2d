#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 diffuser_parameters.py

foamCleanTutorials

restore0Dir
blockMesh
sh transform_stl.sh
surfaceFeatureExtract

cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite
runParallel extrudeMesh

restore0Dir -processor

runParallel checkMesh

touch open.foam

#runParallel pimpleFoam
runParallel simpleFoam
