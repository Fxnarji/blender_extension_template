import bpy
import requests
import requests

from ...constants import get_manifest, get_repo_api, get_preferences
from ...constants import AddonProperties


def check_newest_github_release():
    try:
        response = requests.get(get_repo_api(), timeout=5)
        if response.status_code == 200:
            data = response.json()
            tag = data.get("tag_name", "").lstrip("v")  # remove leading 'v' if present
            latest_version = tuple(map(int, tag.split(".")))
            return latest_version

    except requests.RequestException as e:
        print(f"Error fetching latest release: {e}")
        return None

def get_current_version():
    manifest = get_manifest()
    current_version = manifest["version"]
    return tuple(int(x) for x in current_version.split("."))

def check_if_needs_update():
    current_version = get_current_version()
    remote_version = check_newest_github_release()

    if remote_version > current_version:
        print("out of date")
        preferences = get_preferences()
        preferences.NeedsUpdate = True
        return True
    else:
        print("all fine")
        return False

def run_update_check( ):
        remote_version = check_newest_github_release()
        local_version = get_current_version()
        if remote_version > local_version:
            AddonProperties.needs_update = True
            AddonProperties.remote_version = remote_version
        return {'FINISHED'}