import bpy
import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore

class WEB_OT_OperatorInstallViteDependency(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_vite_dependency_via_npm_operator"
    bl_label = "Install Vite via npm operator"
    bl_description = "Install Vite as a development dependency in your project"

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-vite-dependency.ps1')

    def get_script_args(self):
        props = bpy.context.scene.my_property_group_pointer
        output_directory = props.output_directory
        return ["-DirectoryPath", output_directory]

    def handle_success(self, result, context):
        node_version = result.get("nodeVersion", "Unknown Node.js version")
        npm_version = result.get("npmVersion", "Unknown npm version")
        directory = result.get("directoryPath", "Unknown directory path")
        command_output = result.get("directoryPath", None)
        msg = "Successfully installed Vite dependency into directory"
        print(msg, npm_version, command_output)
        self.report({'INFO'}, f"{msg} {directory} using Node.js {node_version} and npm {npm_version}.")
        create_generic_popup(message=f"{msg},,CHECKMARK|{directory},,CHECKMARK|node version: {node_version},,CHECKMARK|npm version: {npm_version},,CHECKMARK")
