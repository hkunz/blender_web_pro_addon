import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_install_base import OperatorInstallBase # type: ignore

class WEB_OT_OperatorInstallThreeJS(OperatorInstallBase):
    bl_idname = "web.blender_web_pro_install_threejs_operator"
    bl_label = "Install Three.js"
    bl_description = "Install Three.js which is a JavaScript library that simplifies the creation and rendering of 3D graphics in the web browser using WebGL"

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-threejs.ps1')

    def get_script_args(self):
        return ["-DirectoryPath", "C:\\Path\\To\\Directory", "-AnotherArg", "Value"]

    def handle_success(self, result):
        version = result.get("version", "Unknown version")
        already_installed = result.get("alreadyInstalled", False)
        choco_path = result.get("chocoPath", "Unknown path")
        source = result.get("source", "Unknown source")
        msg = "Chocolatey already installed" if already_installed else "Chocolatey installed successfully"
        print(msg, version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Version: {version},,CHECKMARK|Path: {choco_path},,CHECKMARK|Info: {source},,CHECKMARK")









#dir_path = self.my_file_input_prop
#    if os.path.isdir(dir_path):