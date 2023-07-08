import pywavefront

scene = pywavefront.Wavefront(
    'blender/Basis.obj',
    strict=True,
    encoding="iso-8859-1",
    parse=True,
)

for name, material in scene.materials.items():
    material.vertices
    print(material.vertices)
