#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

python3 diffuser_main.py 

cd diffuser_design
sh config_control.sh
cd ..
