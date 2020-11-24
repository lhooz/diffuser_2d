#!/bin/bash
cd constant
cd triSurface
surfaceTransformPoints -scale '(0.2 0.2 1)' tunner_vane.stl vane0.stl
surfaceTransformPoints -rollPitchYaw '(0 0 -50)' vane0.stl vane0.stl
surfaceTransformPoints -translate '(0.767 0 0)' vane0.stl vane1.stl
surfaceTransformPoints -translate '(0 -0.433 0)' vane1.stl vane1.stl
surfaceTransformPoints -translate '(0.933 0 0)' vane0.stl vane2.stl
surfaceTransformPoints -translate '(0 -0.267 0)' vane2.stl vane2.stl
surfaceTransformPoints -translate '(1.1 0 0)' vane0.stl vane3.stl
surfaceTransformPoints -translate '(0 -0.1 0)' vane3.stl vane3.stl
surfaceTransformPoints -translate '(1.27 0 0)' vane0.stl vane4.stl
surfaceTransformPoints -translate '(0 0.0667 0)' vane4.stl vane4.stl
surfaceTransformPoints -translate '(1.43 0 0)' vane0.stl vane5.stl
surfaceTransformPoints -translate '(0 0.233 0)' vane5.stl vane5.stl
cd ..
cd ..
