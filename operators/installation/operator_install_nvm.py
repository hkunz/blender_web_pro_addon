import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore

class WEB_OT_OperatorInstallNVM(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_nvm_operator"
    bl_label = "Install NVM"
    bl_description = "Install NVM (Node Version Manager) which is a tool for managing multiple versions of Node.js on a single machine, allowing users to easily switch between different versions for different projects"

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-nvm.ps1')

    def handle_success(self, result, context):
        nvm_version = result.get("nvmVersion", "Unknown NVM version")
        already_installed = result.get("alreadyInstalled", False)

        msg = "NVM is installed successfully"
        if already_installed:
            msg = "NVM is already installed"

        props = context.scene.installation_props
        props.installation_status_nvm = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_nvm_v = nvm_version

        print(msg, nvm_version)
        create_generic_popup(message=f"{msg},,CHECKMARK|nvm version: {nvm_version},,CHECKMARK")
