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
        result = None
        try:
            result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        output_lines = result.stdout.splitlines()
        success = output_lines[0] == "1"
        if not success:
            error = output_lines[1]
            exception = output_lines[2]
            create_generic_popup(message=f"Chocolatey installation failed,,CANCEL,,1|{error},,CANCEL,,1|{exception},,CANCEL,,1")
            return

        version = output_lines[1]
        already_installed = output_lines[2] == "1"
        choco_path = output_lines[3]
        source = output_lines[4]

        msg = "Unknown State"
        if already_installed:
            msg = f"Chocolatey already installed"
        elif success:
            msg = f"Chocolatey installed successfully"

        print(msg, version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Version: {version},,CHECKMARK|Path: {choco_path},,CHECKMARK|Info: {source},,CHECKMARK")

    def execute(self, _context):
        self.install_choco()
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return True
