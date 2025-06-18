import bpy
import tomllib
import os

#Operators
from .operators.OBJECT_OT_Sample    import OBJECT_OT_Sample 

#panels
from .panels.VIEW3D_PT_UI_Sample      import VIEW3D_PT_UI_Sample

#reading values such as name, version and more from toml so there is no need to change information in two places
def load_manifest_info():
    toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
    with open(toml_path, "rb") as f:
        manifest = tomllib.load(f)

    #reading addon name
    extension_name = manifest["name"]

    #reading addon version
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

    #reading Blender version
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

    bl_info = {
    "name": extension_name,
    "version": version_tuple, 
    "blender": blender_version_tuple,
    }

    return bl_info

manifest = load_manifest_info()
bl_info = {
    "name": manifest["name"],
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Your Name", #(excellent movie)
    "version": manifest["version"], 
    "blender": manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
    #operators:
    OBJECT_OT_Sample,

    #panels:
    VIEW3D_PT_UI_Sample

    ]



def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register() 