import bpy
import os
import requests
import tempfile

from ...constants import AddonProperties, get_repo_api
from ...constants import get_operator
   
class ADDON_OT_update_addon(bpy.types.Operator):
    bl_idname = get_operator("update")
    bl_label = "update_addon"


    def download_latest_release(self, release):
        response = requests.get(get_repo_api(), timeout=5)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch release data: {response.status_code}")

        release = response.json()


        # [0] always downloads the first asset in the release page. 
        # The manual release github action automatically adds the files in the right way, 
        # but if you manually add more be careful
        assets = release.get("assets", [])
        new_build = assets[0]
        asset_url = new_build["browser_download_url"]
        asset_name = new_build["name"]

        #downloads the new build by default into /tmp
        temp_path = tempfile.gettempdir()
        asset_path = os.path.join(temp_path, asset_name)

        asset_response = requests.get(asset_url)
        with open(asset_path, "wb") as f:
            f.write(asset_response.content)
        return asset_path
    
    def install_new_version(self,path):
        #installs, enables the addon and saves preferences
        bpy.ops.preferences.addon_install(filepath=path, overwrite=True)
        bpy.ops.preferences.addon_enable(module = AddonProperties.module_name)
        bpy.ops.wm.save_userpref()

    def execute(self, context):
        remote_version = AddonProperties.remote_version
        zip_path = self.download_latest_release(remote_version)
        self.install_new_version(zip_path)
        return {'FINISHED'}