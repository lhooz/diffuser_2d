#!/bin/bash

foamCleanTutorials
sh transform_stl.sh
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite | tee log.snappyHexMesh
extrudeMesh

checkMesh |  tee log.checkMesh

touch open.foam
