#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

rm -r 0
python3 tube_parameters.py

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

runParallel checkMesh
touch open.foam
