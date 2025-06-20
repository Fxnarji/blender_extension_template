import bpy
import requests
import tempfile
import os
import requests

from ...constants import AddonProperties, get_manifest, get_repo_api, get_preferences
from ...constants import get_operator   
class ADDON_OT_update_addon(bpy.types.Operator):
    bl_idname = get_operator("update")
    bl_label = "update_addon"


    def download_latest_release(self, release):
        response = requests.get(get_repo_api(), timeout=5)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch release data: {response.status_code}")

        release = response.json()

        for asset in release.get("assets", []):
            asset_url = asset["browser_download_url"]
            asset_name = asset["name"]
            print(asset_name)
            temp_path = tempfile.gettempdir()
            asset_path = os.path.join(temp_path, asset_name)

            print(f"Downloading asset: {asset_name}")
            asset_response = requests.get(asset_url)
            with open(asset_path, "wb") as f:
                f.write(asset_response.content)
            print(f"Saved asset to {asset_path}")
        return asset_path
    
    def install_new_version(path):
        bpy.ops.preferences.addon_install(filepath=path, overwrite=True)
        bpy.ops.preferences.addon_enable(module = AddonProperties.module_name)
        bpy.ops.wm.save_userpref()

    def execute(self, context):
        remote_version = AddonProperties.remote_version
        print(remote_version)
        zip_path = self.download_latest_release(remote_version)
        self.install_new_version(zip_path)
        print(AddonProperties.remote_version)

        return {'FINISHED'}