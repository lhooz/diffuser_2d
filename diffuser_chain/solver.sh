#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

cd diffuder_design
cd diffuser_main

restore0Dir -processor

runParallel checkMesh

touch open.foam

#runParallel pimpleFoam
runParallel simpleFoam

cd ..
cd ..
