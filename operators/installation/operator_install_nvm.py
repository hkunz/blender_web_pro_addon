import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorInstallNVM(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_nvm_operator"
    bl_label = "Install Node Version Manager (NVM)"
    bl_description = "Install NVM (Node Version Manager) which is a tool for managing multiple versions of Node.js on a single machine, allowing users to easily switch between different versions for different projects"

    def draw(self, context) -> None:
        self.message = "Proceed with Node Version Manager Installation?|This may take several minutes.,,INFO|Please wait while installation completes.,,INFO"
        self.exec_message = "Installing Node Version manager ... Please wait ..."
        super().draw(context)

    def get_log_file(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'logs/install-nvm.log')

    def get_script_path(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/windows', 'install-nvm.ps1')

    def handle_success(self, result, context):
        nvm_version = result.get("nvmVersion", "Unknown NVM version")
        already_installed = result.get("alreadyInstalled", False)

        msg = "Node Version Manager (NVM) is installed successfully"
        if already_installed:
            msg = "Node Version Manager (NVM) is already installed"

        props = context.scene.installation_props
        props.installation_status_nvm = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_nvm_v = nvm_version

        create_generic_popup(message=f"{msg},,CHECKMARK|nvm version: {nvm_version},,CHECKMARK")

    @classmethod
    def poll(cls, context):
        props: InstallationPropertyGroup = context.scene.installation_props
        return props.installed_nodejs_v != "" and props.installed_choco_v != ""
