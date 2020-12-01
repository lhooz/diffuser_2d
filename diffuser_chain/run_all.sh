#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

sh mesh.sh
sh solver.sh
