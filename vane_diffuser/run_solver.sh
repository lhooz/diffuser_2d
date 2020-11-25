#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

restore0Dir -processor

runParallel checkMesh

touch open.foam

#runParallel pimpleFoam
runParallel simpleFoam
