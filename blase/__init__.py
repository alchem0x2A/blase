# check if bpy can be imported
import warnings
try:
    import bpy
except ImportError:
    warnings.warn("The module bpy cannot be imported. Please use the Blender-bundled python for generating files.")

