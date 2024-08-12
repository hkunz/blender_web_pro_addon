import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore

class WEB_OT_OperatorInstallChoco(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_choco_operator"
    bl_label = "Install Chocolatey"
    bl_description = "Install Chocolatey which is a package manager for Windows that simplifies the installation, update, and management of software packages and dependencies"

    def __init__(self):
        super().__init__()
        #FIXME: https://blender.stackexchange.com/questions/322779/how-can-i-get-info-report-to-show-up-before-subprocess-call
        #msg = "Installing Chocolatey... Please be patient as this may take a few moments."
        #print(msg)
        #self.report({'INFO'}, msg)

    def draw(self, context) -> None:
        self.message = "Proceed with Chocolatey Installation?"
        self.exec_message = "Installing Chocolatey... Please wait..."
        super().draw(context)

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-choco.ps1')

    def handle_success(self, result, context):
        version = result.get("version", "Unknown version")
        already_installed = result.get("alreadyInstalled", False)
        choco_path = result.get("chocoPath", "Unknown path")
        source = result.get("source", "Unknown source")
        msg = "Chocolatey is already installed" if already_installed else "Chocolatey is installed successfully"
        props = context.scene.installation_props
        props.installation_status_choco = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_choco_v = version
        print(msg, version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Version: {version},,CHECKMARK|Path: {choco_path},,CHECKMARK|Info: {source},,CHECKMARK")
