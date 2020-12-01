#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 diffuser_parameters.py

foamCleanTutorials

runApplication blockMesh

sh transform_stl.sh
runApplication surfaceFeatureExtract

cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite

runParallel extrudeMesh

sh transform_mesh.sh

runApplication reconstructParMesh -constant -latestTime -mergeTol 1e-6

runApplication checkMesh

touch open.foam
