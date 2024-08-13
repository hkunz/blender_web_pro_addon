import bpy
import os
import platform
import subprocess

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorInstallCheck(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_check_operator"
    bl_label = "Check Installation Prerequisites"
    bl_description = "Check installation status"
    bl_options = {'REGISTER'}

    def get_log_file(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'logs/install-check.log')

    def get_script_path(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/windows', 'install-check.ps1')

    def draw(self, context) -> None:
        self.message = "Check if all prerequisites are installed?|This may take a few moments.,,INFO"
        self.exec_message = "Checking prerequisites... Please wait..."
        super().draw(context)

    def execute_script(self, context):
        self.set_execution_policy()
        super().execute_script(context)

    def set_execution_policy(self, policy='RemoteSigned', scope='CurrentUser'):
        # if command 'Get-ExecutionPolicy' yields 'Restricted' you will have to execute 'Set-ExecutionPolicy RemoteSigned' manually or through this function in order to be able to run scripts on windows
        if platform.system() != 'Windows':
            print("This script can only be run on Windows.")
            return
        command = (
            f'Write-Host "{os.path.abspath(__file__)}" -ForegroundColor Blue; '
            '$psVersion = "$($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor).$($PSVersionTable.PSVersion.Build)"; '
            'Write-Host "PowerShell version: $psVersion" -ForegroundColor Cyan; '
            f'$cmd = "Set-ExecutionPolicy {policy} -Scope {scope} -Force"; '
            'Write-Host "Executing command: $cmd" -ForegroundColor White; '
            'Invoke-Expression $cmd; '
            '$output = Get-ExecutionPolicy; '
            'Write-Host "Get-ExecutionPolicy is set to $output" -ForegroundColor Yellow'
        )

        try:
            result = subprocess.run(['powershell', '-Command', command], capture_output=False, text=True, check=True)
            self.report({'INFO'}, f"Execution policy set to {policy} successfully.")
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Failed to set execution policy. Error: {e.stderr}")

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

        errors = result.get("errors")
        if not errors or not len(errors):
            return
        for line in errors:
            self.report({'ERROR'}, line)
        create_generic_popup(message=f"There are errors in your installation,,CANCEL,,1|Please check the Info Panel for the errors.,,TRIA_RIGHT")


