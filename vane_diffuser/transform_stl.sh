#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.11 0.11 1)' basic_vane.stl single_vanem.stl
surfaceTransformPoints -scale '(0.11 0.11 1)' diffuser_wall.stl dwall.stl
surfaceTransformPoints -rollPitchYaw '(0 0 17.2)' single_vanem.stl single_vaneu.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -17.2)' single_vanem.stl single_vanel.stl
surfaceTransformPoints -rollPitchYaw '(0 0 25)' dwall.stl dwallu.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -25)' dwall.stl dwalll.stl
surfaceTransformPoints -translate '(0 0.033 0)' single_vaneu.stl single_vaneu.stl
surfaceTransformPoints -translate '(0 -0.033 0)' single_vanel.stl single_vanel.stl
surfaceTransformPoints -translate '(0 0.0605 0)' dwallu.stl dwallu.stl
surfaceTransformPoints -translate '(0 -0.0605 0)' dwalll.stl dwalll.stl
cd ..
cd ..
