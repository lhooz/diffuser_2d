#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 tube_parameters.py

foamCleanTutorials

blockMesh

sh transform_stl.sh
surfaceFeatureExtract

cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite

runParallel extrudeMesh

sh transform_mesh.sh

runParallel checkMesh

touch open.foam
