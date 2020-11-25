#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 tunner_parameters.py

foamCleanTutorials
blockMesh
sh transform_stl.sh
surfaceFeatureExtract

cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite
#restore0Dir -processor
runParallel extrudeMesh

checkMesh |  tee log.checkMesh

touch open.foam
