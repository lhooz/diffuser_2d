#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

runParallel mergeMeshes . ../tunner -overwrite
touch open.foam
