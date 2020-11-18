#!/bin/bash
python3 diffuser_parameters.py

foamCleanTutorials
sh transform_stl.sh
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite | tee log.snappyHexMesh
extrudeMesh

rm -r 0
cp -r 0_org 0

checkMesh |  tee log.checkMesh

touch open.foam

decomposePar
mpirun -np 4 renumberMesh -overwrite -parallel | tee log.renumberMesh
mpirun -np 4 simpleFoam -parallel | tee log.solver
