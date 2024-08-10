import bpy
import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_install_base import OperatorInstallBase # type: ignore

class WEB_OT_OperatorInstallThreeJS(OperatorInstallBase):
    bl_idname = "blender_web_pro.install_threejs_operator"
    bl_label = "Install Three.js"
    bl_description = "Install Three.js which is a JavaScript library that simplifies the creation and rendering of 3D graphics in the web browser using WebGL"

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-threejs.ps1')

    def get_script_args(self):
        props = bpy.context.scene.my_property_group_pointer  # Adjust this if your property group is located elsewhere
        output_directory = props.output_directory
        return ["-DirectoryPath", output_directory, "-AnotherArg", "Value22"]

    def handle_success(self, result):
        npm_version = result.get("npmVersion", "Unknown npm version")
        directory = result.get("directoryPath", "Unknown directory path")
        command_output = result.get("directoryPath", None)
        msg = "Successfully installed Three.JS into directory"
        print(msg, npm_version, command_output)
        self.report({'INFO'}, f"{msg} {directory} using npm version {npm_version}.")
        create_generic_popup(message=f"{msg},,CHECKMARK|{directory},,CHECKMARK|npm version: {npm_version},,CHECKMARK")









#dir_path = self.my_file_input_prop
#    if os.path.isdir(dir_path):