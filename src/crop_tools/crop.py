#!/usr/bin/env python3

from scyjava import jimport

print("loading java classes")
MeshCroppingTool = jimport('deformablemesh.geometry.MeshCroppingTool')
Paths = jimport('java.nio.file.Paths')

tool = MeshCroppingTool(1.5, 48)

image = Paths.get(sys.argv[1])
meshes = Paths.get(sys.argv[2])

print("processing %s and %s"%(image, meshes) )
tool.processMeshImages(image, meshes)

print("made it to here!")
