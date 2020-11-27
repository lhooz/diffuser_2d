#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.2 0.1 1)' tube_wall.stl tbwall.stl
cd ..
cd ..
