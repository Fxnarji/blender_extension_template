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
        print(assets)
        new_build = assets[0]
        print(new_build)
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
        print(zip_path)
        #self.install_new_version(zip_path)
        return {'FINISHED'}
    


    [{'url': 'https://api.github.com/repos/Fxnarji/blender_extension_template/releases/assets/265728249', 
      'id': 265728249, 'node_id': 'RA_kwDOO-D7rc4P1rD5', 'name': 'blender_extension_template_1.0.9.zip', 
      'label': '', 'uploader': 
      {'login': 'github-actions[bot]', 
       'id': 41898282, 'node_id': 
       'MDM6Qm90NDE4OTgyODI=', 
       'avatar_url': 'https://avatars.githubusercontent.com/in/15368?v=4', 
       'gravatar_id': '', 
       'url': 'https://api.github.com/users/github-actions%5Bbot%5D', 
       'html_url': 'https://github.com/apps/github-actions', 'followers_url': 
       'https://api.github.com/users/github-actions%5Bbot%5D/followers', 
       'following_url': 'https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}', 
       'gists_url': 'https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}', 
       'starred_url': 'https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}', 
       'subscriptions_url': 'https://api.github.com/users/github-actions%5Bbot%5D/subscriptions', 
       'organizations_url': 'https://api.github.com/users/github-actions%5Bbot%5D/orgs', ''
       'repos_url': 'https://api.github.com/users/github-actions%5Bbot%5D/repos', 'events_url':
         'https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}', 'received_events_url': 
         'https://api.github.com/users/github-actions%5Bbot%5D/received_events', 
         'type': 'Bot', 
         'user_view_type': 'public',
         'site_admin': False},

         'content_type': 'application/zip', 
         'state': 'uploaded', 
         'size': 6195, 
         'digest': 'sha256:43a7523bbe3c1c35dd646190981e5f236014df917d1099182bf953837cdc1d9a', 
         'download_count': 1, 
         'created_at': '2025-06-20T12:46:56Z', 
         'updated_at': '2025-06-20T12:46:56Z', 
         'browser_download_url': 'https://github.com/Fxnarji/blender_extension_template/releases/download/1.0.9/blender_extension_template_1.0.9.zip'}]