#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

cd diffuser_design
cd 0_diffuser_main

restore0Dir -processor

#cp -f system/fvSchemes.pimpleFoam system/fvSchemes
#runParallel potentialFoam -writep
#runParallel pimpleFoam

cp -f system/fvSchemes.simpleFoam system/fvSchemes
runParallel potentialFoam -writep
runParallel simpleFoam

cd ..
cd ..
