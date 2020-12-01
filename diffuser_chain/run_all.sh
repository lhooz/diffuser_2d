#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

sh main_mesh.sh
sh main_solver.sh
