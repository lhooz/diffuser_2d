#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -translate '(0 -0.5 0)' tunner_wall.stl twall.stl
surfaceTransformPoints -scale '(0.1 0.1 1)' twall.stl twall.stl
surfaceTransformPoints -scale '(0.02 0.02 1)' tunner_vane.stl vane0.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -49)' vane0.stl vane0.stl
surfaceTransformPoints -translate '(0.0267 0 0)' vane0.stl vane1.stl
surfaceTransformPoints -translate '(0 -0.0433 0)' vane1.stl vane1.stl
surfaceTransformPoints -translate '(0.0433 0 0)' vane0.stl vane2.stl
surfaceTransformPoints -translate '(0 -0.0267 0)' vane2.stl vane2.stl
surfaceTransformPoints -translate '(0.06 0 0)' vane0.stl vane3.stl
surfaceTransformPoints -translate '(0 -0.01 0)' vane3.stl vane3.stl
surfaceTransformPoints -translate '(0.0767 0 0)' vane0.stl vane4.stl
surfaceTransformPoints -translate '(0 0.00667 0)' vane4.stl vane4.stl
surfaceTransformPoints -translate '(0.0933 0 0)' vane0.stl vane5.stl
surfaceTransformPoints -translate '(0 0.0233 0)' vane5.stl vane5.stl
cd ..
cd ..
