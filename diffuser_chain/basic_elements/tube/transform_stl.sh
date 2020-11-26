#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.5 0.1 1)' tube_wall.stl tbwall.stl
cd ..
cd ..
