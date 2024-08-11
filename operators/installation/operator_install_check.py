import bpy
import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore

class WEB_OT_OperatorInstallCheck(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_check_operator"
    bl_label = "Installation Check Operator"
    bl_description = "Check installation status"
    bl_options = {'REGISTER'}

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-check.ps1')

    def handle_success(self, result, context):
        props = context.scene.installation_props
        props.check_installation = False

        props.installation_status_choco = result.get("choco", InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED)
        props.installation_status_nodejs = result.get("node", InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED)
        props.installation_status_npx = result.get("npx", InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED)
        props.installation_status_npm = result.get("npm", InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED)
        props.installation_status_nvm = result.get("nvm", InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED)

        props.installed_choco_v = result.get("choco_version", "Unknown Version")
        props.installed_nodejs_v = result.get("node_version", "Unknown Version")
        props.installed_npm_v = result.get("npm_version", "Unknown Version")
        props.installed_npx_v = result.get("npx_version", "Unknown Version")
        props.installed_nvm_v = result.get("nvm_version", "Unknown Version")
