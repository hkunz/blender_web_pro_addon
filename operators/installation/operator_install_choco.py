import subprocess
import platform
import os
import bpy

from blender_web_pro.utils.file_utils import FileUtils # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore

class WEB_OT_OperatorInstallChoco(bpy.types.Operator):
    bl_idname = "web.blender_web_pro_install_choco_operator"
    bl_label = "Install Chocolatey"
    bl_description = "Install Chocolatey which is a package manager for Windows that simplifies the installation, update, and management of software packages and dependencies."
    bl_options = {'INTERNAL'}

    def install_choco(self):
        script_path = os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-choco.ps1')

        try:
            result = subprocess.run(
                ["powershell", "-File", script_path],
                capture_output=True, text=True, check=True
            )
            output_lines = result.stdout.splitlines()
            success = False
            version = None

            success = output_lines[0] == "1"       # Element 0: 1 for success, 0 for fail
            version = output_lines[1]              # Element 1: Version string
            already_installed = output_lines[2] == "1"     # Element 2: 1 if already installed, 0 if newly installed
            choco_path = output_lines[3]

            return success, version, already_installed, choco_path
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return 0, None, 0, "No Path"

    def execute(self, _context):
        success, version, already_installed, choco_path = self.install_choco()
        if already_installed:
            print(f"Chocolatey already installed: {version}")
            #create_generic_popup(message=f"Chocolatey already installed|Version: {version}")
            create_generic_popup(message=f"Chocolatey is already installed,,CHECKMARK|Version: {version}|Path: {choco_path}|Info: https://community.chocolatey.org/install.ps1")
        elif success:
            create_generic_popup(message=f"Chocolatey is installed successfully,,CHECKMARK|Version: {version}|Path: {choco_path}|Info: https://community.chocolatey.org/install.ps1")
        else:
            print("Script execution failed.")
            create_generic_popup(message=f"Chocolatey installation failed,,CANCEL,,1|File:")
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return True
