import subprocess
import os
import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore

class WEB_OT_OperatorInstallNodeJS(bpy.types.Operator):
    bl_idname = "web.blender_web_pro_install_nodejs_choco_operator"
    bl_label = "Install NodeJS LTS"
    bl_description = "Install Node.js via Chocolatey, which includes both the Node.js runtime and npm, which is the default package manager for Node.js."
    bl_options = {'INTERNAL'}

    def install_nodejs_choco(self):
        script_path = os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-nodejs-choco.ps1')
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
            create_generic_popup(message=f"NodeJS installation via Chocolatey failed,,CANCEL,,1|{error},,CANCEL,,1|{exception},,CANCEL,,1")
            return

        version = output_lines[1]
        already_installed = output_lines[2] == "1"

        msg = "Unknown State"
        if already_installed:
            msg = f"NodeJS already installed"
        elif success:
            msg = f"NodeJS installed successfully"

        print(msg, version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Version: {version},,CHECKMARK")

    def execute(self, _context):
        self.install_nodejs_choco()
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return True
