# trace generated using paraview version 5.7.0
#
# To ensure correct image size when batch processing, please search
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
import os
import shutil
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1457, 678]

# destroy renderView1
Delete(renderView1)
del renderView1

# load state
cwd = os.getcwd()
pvstate_file = os.path.join(
    cwd, 'diffuser_design/0_diffuser_main/paraview/machpost.pvsm')
datadir = os.path.join(cwd, 'diffuser_design/0_diffuser_main/paraview')
foam_file = os.path.join(cwd, 'diffuser_design/0_diffuser_main/open.foam')

output_folder = os.path.join(cwd, 'pv_results')
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.mkdir(output_folder)

LoadState(pvstate_file,
          LoadStateDataFileOptions='Choose File Names',
          DataDirectory=datadir,
          openfoamFileName=foam_file,
          openfoam1FileName=foam_file,
          openfoam2FileName=foam_file)

# find view
spreadSheetView1 = FindViewOrCreate('SpreadSheetView1',
                                    viewtype='SpreadSheetView')
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1457, 678]

# set active view
SetActiveView(renderView1)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [
    0.17210149765014648, -0.09620611369609833, 3.224740768459531
]
renderView1.CameraFocalPoint = [0.17210149765014648, -0.09620611369609833, 0.0]
renderView1.CameraParallelScale = 0.5700596451033839
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(
    os.path.join(output_folder, 'mach.png'),
    renderView1,
    ImageResolution=[1457, 678],
    OverrideColorPalette='WhiteBackground',
    # PNG options
    CompressionLevel='0')

# find source
totalpressure = FindSource('Totalpressure')

# set active source
SetActiveSource(totalpressure)

# show data in view
totalpressureDisplay = Show(totalpressure, renderView1)

# trace defaults for the display properties.
totalpressureDisplay.Representation = 'Surface'

# show color bar/color legend
totalpressureDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Totalp'
totalpLUT = GetColorTransferFunction('Totalp')

# get opacity transfer function/opacity map for 'Totalp'
totalpPWF = GetOpacityTransferFunction('Totalp')

# find source
mach = FindSource('Mach')

# hide data in view
Hide(mach, renderView1)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [
    0.17210149765014648, -0.09620611369609833, 3.224740768459531
]
renderView1.CameraFocalPoint = [0.17210149765014648, -0.09620611369609833, 0.0]
renderView1.CameraParallelScale = 0.5700596451033839
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(
    os.path.join(output_folder, 'totalp.png'),
    renderView1,
    ImageResolution=[1457, 678],
    OverrideColorPalette='WhiteBackground',
    # PNG options
    CompressionLevel='0')

# find source
p = FindSource('p')

# set active source
SetActiveSource(p)

# show data in view
pDisplay = Show(p, renderView1)

# trace defaults for the display properties.
pDisplay.Representation = 'Surface'

# show color bar/color legend
pDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# hide data in view
Hide(totalpressure, renderView1)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [
    0.17210149765014648, -0.09620611369609833, 3.224740768459531
]
renderView1.CameraFocalPoint = [0.17210149765014648, -0.09620611369609833, 0.0]
renderView1.CameraParallelScale = 0.5700596451033839
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(
    os.path.join(output_folder, 'p.png'),
    renderView1,
    ImageResolution=[1457, 678],
    OverrideColorPalette='WhiteBackground',
    # PNG options
    CompressionLevel='0')

# set active source
SetActiveSource(p)

# find source
openfoam = FindSource('open.foam')

# set active source
SetActiveSource(openfoam)

# set active view
SetActiveView(spreadSheetView1)

# find source
aveMach_inlet = FindSource('Ave.Mach_inlet')

# set active source
SetActiveSource(aveMach_inlet)

# show data in view
aveMach_inletDisplay = Show(aveMach_inlet, spreadSheetView1)

# show data in view
aveMach_inletDisplay = Show(aveMach_inlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'Inlet_mach.csv'),
           view=spreadSheetView1)

# find source
avep_inlet = FindSource('Ave.p_inlet')

# set active source
SetActiveSource(avep_inlet)

# show data in view
avep_inletDisplay = Show(avep_inlet, spreadSheetView1)

# show data in view
avep_inletDisplay = Show(avep_inlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'inlet_p.csv'), view=spreadSheetView1)

# find source
avetotalp_inlet = FindSource('Ave.totalp_inlet')

# set active source
SetActiveSource(avetotalp_inlet)

# show data in view
avetotalp_inletDisplay = Show(avetotalp_inlet, spreadSheetView1)

# show data in view
avetotalp_inletDisplay = Show(avetotalp_inlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'inlet_totalp.csv'),
           view=spreadSheetView1)

# find source
aveMach_outlet = FindSource('Ave.Mach_outlet')

# set active source
SetActiveSource(aveMach_outlet)

# show data in view
aveMach_outletDisplay = Show(aveMach_outlet, spreadSheetView1)

# show data in view
aveMach_outletDisplay = Show(aveMach_outlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'outlet_mach.csv'),
           view=spreadSheetView1)

# find source
avep_outlet = FindSource('Ave.p_outlet')

# set active source
SetActiveSource(avep_outlet)

# show data in view
avep_outletDisplay = Show(avep_outlet, spreadSheetView1)

# show data in view
avep_outletDisplay = Show(avep_outlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'outlet_p.csv'), view=spreadSheetView1)

# find source
avetotalp_outlet = FindSource('Ave.totalp_outlet')

# set active source
SetActiveSource(avetotalp_outlet)

# show data in view
avetotalp_outletDisplay = Show(avetotalp_outlet, spreadSheetView1)

# show data in view
avetotalp_outletDisplay = Show(avetotalp_outlet, spreadSheetView1)

# export view
ExportView(os.path.join(output_folder, 'outlet_totalp.csv'),
           view=spreadSheetView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [
    0.17210149765014648, -0.09620611369609833, 3.224740768459531
]
renderView1.CameraFocalPoint = [0.17210149765014648, -0.09620611369609833, 0.0]
renderView1.CameraParallelScale = 0.5700596451033839
renderView1.CameraParallelProjection = 1

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
