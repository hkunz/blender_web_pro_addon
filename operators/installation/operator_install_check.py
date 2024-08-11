import bpy
import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore

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
        return
        nvm_version = result.get("nvmVersion", "Unknown NVM version")
        already_installed = result.get("alreadyInstalled", False)

        msg = "NVM is installed successfully"
        if already_installed:
            msg = "NVM is already installed"

        print(msg, nvm_version)
        create_generic_popup(message=f"{msg},,CHECKMARK|nvm version: {nvm_version},,CHECKMARK")
