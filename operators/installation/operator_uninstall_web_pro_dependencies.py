import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

# Enable "Developer Extras" or bpy.context.preferences.view.show_developer_ui = True to use F3 > Search Operator

class WEB_OT_OperatorUninstallWebProDependencies(OperatorScriptBase):
    bl_idname = "blender_web_pro.uninstall_dependencies"
    bl_label = "Uninstall Blender Web Pro Dependencies"
    bl_description = "Uninstall all dependencies related to Blender Web Pro, including Chocolatey, Node.js, NVM, and more."
    bl_options = {'REGISTER'}

    def draw(self, context) -> None:
        self.message = "Are you sure you want to uninstall the following?|Chocolatey,,CHECKBOX_DEHLT|Node.js,,CHECKBOX_DEHLT|Node Version Manager (NVM),,CHECKBOX_DEHLT"
        self.exec_message = "Uninstalling Chocolatey, Node.js, NVM ... Please wait ..."
        super().draw(context)

    def get_log_file(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'logs/uninstall-web-pro-dependencies.log')

    def get_script_path(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/windows', 'uninstall-web-pro-dependencies.ps1')

    def handle_success(self, result, context):
        no_choco_installed = result.get("no_choco_installed", False)
        props = context.scene.installation_props
        props.installation_status_choco = InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED
        props.installation_status_nodejs = InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED
        props.installation_status_nvm = InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED
        props.installed_choco_v = ""
        props.installed_nodejs_v = ""
        props.installed_npm_v = ""
        print("Unintsalled Chocolate, Node.js, Node Version Manager (NVM) successfully")
        message = "Chocolatey is not installed|No directory: 'C:\ProgramData\chocolatey' found" if no_choco_installed else f"Uninstalled the following Web Pro Dependencies:|Chocolatey,,CHECKMARK|Node.js,,CHECKMARK|Node Version Manager (NVM),,CHECKMARK"
        create_generic_popup(message=message)
