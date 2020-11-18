#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.1 0.1 1)' tunner_vane.stl vane0.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -45)' vane0.stl vane0.stl
surfaceTransformPoints -translate '(1.1 0 0)' vane0.stl vane1.stl
surfaceTransformPoints -translate '(0 -0.497 0)' vane1.stl vane1.stl
surfaceTransformPoints -translate '(1.16 0 0)' vane0.stl vane2.stl
surfaceTransformPoints -translate '(0 -0.445 0)' vane2.stl vane2.stl
surfaceTransformPoints -translate '(1.21 0 0)' vane0.stl vane3.stl
surfaceTransformPoints -translate '(0 -0.392 0)' vane3.stl vane3.stl
surfaceTransformPoints -translate '(1.26 0 0)' vane0.stl vane4.stl
surfaceTransformPoints -translate '(0 -0.339 0)' vane4.stl vane4.stl
surfaceTransformPoints -translate '(1.31 0 0)' vane0.stl vane5.stl
surfaceTransformPoints -translate '(0 -0.287 0)' vane5.stl vane5.stl
surfaceTransformPoints -translate '(1.37 0 0)' vane0.stl vane6.stl
surfaceTransformPoints -translate '(0 -0.234 0)' vane6.stl vane6.stl
surfaceTransformPoints -translate '(1.42 0 0)' vane0.stl vane7.stl
surfaceTransformPoints -translate '(0 -0.182 0)' vane7.stl vane7.stl
surfaceTransformPoints -translate '(1.47 0 0)' vane0.stl vane8.stl
surfaceTransformPoints -translate '(0 -0.129 0)' vane8.stl vane8.stl
surfaceTransformPoints -translate '(1.52 0 0)' vane0.stl vane9.stl
surfaceTransformPoints -translate '(0 -0.0763 0)' vane9.stl vane9.stl
surfaceTransformPoints -translate '(1.58 0 0)' vane0.stl vane10.stl
surfaceTransformPoints -translate '(0 -0.0237 0)' vane10.stl vane10.stl
surfaceTransformPoints -translate '(1.63 0 0)' vane0.stl vane11.stl
surfaceTransformPoints -translate '(0 0.0289 0)' vane11.stl vane11.stl
surfaceTransformPoints -translate '(1.68 0 0)' vane0.stl vane12.stl
surfaceTransformPoints -translate '(0 0.0816 0)' vane12.stl vane12.stl
surfaceTransformPoints -translate '(1.73 0 0)' vane0.stl vane13.stl
surfaceTransformPoints -translate '(0 0.134 0)' vane13.stl vane13.stl
surfaceTransformPoints -translate '(1.79 0 0)' vane0.stl vane14.stl
surfaceTransformPoints -translate '(0 0.187 0)' vane14.stl vane14.stl
surfaceTransformPoints -translate '(1.84 0 0)' vane0.stl vane15.stl
surfaceTransformPoints -translate '(0 0.239 0)' vane15.stl vane15.stl
surfaceTransformPoints -translate '(1.89 0 0)' vane0.stl vane16.stl
surfaceTransformPoints -translate '(0 0.292 0)' vane16.stl vane16.stl
surfaceTransformPoints -translate '(1.94 0 0)' vane0.stl vane17.stl
surfaceTransformPoints -translate '(0 0.345 0)' vane17.stl vane17.stl
surfaceTransformPoints -translate '(2 0 0)' vane0.stl vane18.stl
surfaceTransformPoints -translate '(0 0.397 0)' vane18.stl vane18.stl
cd ..
cd ..
