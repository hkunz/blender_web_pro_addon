import bpy
import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_install_dependency import WEB_OT_OperatorInstallDependency # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorInstallThreeJS(WEB_OT_OperatorInstallDependency):
    bl_idname = "blender_web_pro.install_threejs_via_npm_operator"
    bl_label = "Install Three.js via NPM"
    bl_description = "Install Three.js (via npm) which is a JavaScript library that simplifies the creation and rendering of 3D graphics in the web browser using WebGL"

    def draw(self, context) -> None:
        self.message = "Proceed with Three.js Installation into directory?|This may take several minutes.,,INFO|Please wait while installation completes.,,INFO"
        self.exec_message = "Installing Three.js ... Please wait ..."
        super().draw(context)

    def get_log_file(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'logs/install-threejs.log')

    def get_script_args(self):
        props = bpy.context.scene.userinterface_props
        output_directory = props.output_directory.strip()
        return ["-DirectoryPath", output_directory, "-install_name", "Three.js", "-logfile", "install-threejs.log", "-command", "& { npm install --save three }"]

    def get_script_path(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/windows', 'install-dependency.ps1')

    def handle_success(self, result, context):
        super().handle_success(result, context)
        node_version = result.get("nodeVersion", "Unknown Node.js version")
        npm_version = result.get("npmVersion", "Unknown npm version")
        directory = result.get("directoryPath", "Unknown directory path")
        msg = "Successfully installed Three.JS into directory"
        self.report({'INFO'}, f"{msg} {directory} using Node.js {node_version} and npm {npm_version}.")
        create_generic_popup(message=f"{msg},,CHECKMARK|{directory},,CHECKMARK|node version: {node_version},,CHECKMARK|npm version: {npm_version},,CHECKMARK")