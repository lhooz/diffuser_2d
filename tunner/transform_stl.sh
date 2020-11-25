#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -translate '(0 -0.5 0)' tunner_wall.stl twall.stl
surfaceTransformPoints -scale '(0.1 0.1 1)' twall.stl twall.stl
surfaceTransformPoints -scale '(0.015 0.015 1)' tunner_vane.stl vane0.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -49)' vane0.stl vane0.stl
surfaceTransformPoints -translate '(0.0215 0 0)' vane0.stl vane1.stl
surfaceTransformPoints -translate '(0 -0.0485 0)' vane1.stl vane1.stl
surfaceTransformPoints -translate '(0.0315 0 0)' vane0.stl vane2.stl
surfaceTransformPoints -translate '(0 -0.0385 0)' vane2.stl vane2.stl
surfaceTransformPoints -translate '(0.0415 0 0)' vane0.stl vane3.stl
surfaceTransformPoints -translate '(0 -0.0285 0)' vane3.stl vane3.stl
surfaceTransformPoints -translate '(0.0515 0 0)' vane0.stl vane4.stl
surfaceTransformPoints -translate '(0 -0.0185 0)' vane4.stl vane4.stl
surfaceTransformPoints -translate '(0.0615 0 0)' vane0.stl vane5.stl
surfaceTransformPoints -translate '(0 -0.00854 0)' vane5.stl vane5.stl
surfaceTransformPoints -translate '(0.0715 0 0)' vane0.stl vane6.stl
surfaceTransformPoints -translate '(0 0.00146 0)' vane6.stl vane6.stl
surfaceTransformPoints -translate '(0.0815 0 0)' vane0.stl vane7.stl
surfaceTransformPoints -translate '(0 0.0115 0)' vane7.stl vane7.stl
surfaceTransformPoints -translate '(0.0915 0 0)' vane0.stl vane8.stl
surfaceTransformPoints -translate '(0 0.0215 0)' vane8.stl vane8.stl
surfaceTransformPoints -translate '(0.101 0 0)' vane0.stl vane9.stl
surfaceTransformPoints -translate '(0 0.0315 0)' vane9.stl vane9.stl
cd ..
cd ..
