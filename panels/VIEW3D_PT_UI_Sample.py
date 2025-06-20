import bpy
from ..constants import AddonProperties
from ..constants import get_operator
         
class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    bl_label = "A Fancy Panel!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category


    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="you can give me a name!", icon = "OUTLINER_DATA_LIGHT")
        box.operator(get_operator("operator"), text = "example operator", icon = "BLENDER")

        row = layout.row()
        row.active = False
        row.label(text = "made by Fxnarji", icon = "SHADERFX")

        row = layout.row()
        row.operator(get_operator("update"), text = "Check for updates", icon = "FILE_REFRESH")

        if AddonProperties.needs_update:
            box = layout.box()
            box.label(text = "update available!")
            box.operator(get_operator("update"), text = "download version " + str(AddonProperties.remote_version))