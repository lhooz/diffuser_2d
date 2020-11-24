#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.11 0.11 1)' basic_vane.stl single_vanem.stl
surfaceTransformPoints -rollPitchYaw '(0 0 17.2)' single_vanem.stl single_vaneu.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -17.2)' single_vanem.stl single_vanel.stl
surfaceTransformPoints -translate '(0 0.033 0)' single_vaneu.stl single_vaneu.stl
surfaceTransformPoints -translate '(0 -0.033 0)' single_vanel.stl single_vanel.stl
cd ..
cd ..
