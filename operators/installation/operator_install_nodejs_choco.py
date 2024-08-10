import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_install_base import OperatorInstallBase # type: ignore

class WEB_OT_OperatorInstallNodeJS(OperatorInstallBase):
    bl_idname = "blender_web_pro.install_nodejs_operator"
    bl_label = "Install Node.js"
    bl_description = "Install Node.js which is a JavaScript runtime built on Chrome's V8 JavaScript engine"

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-nodejs-choco.ps1')

    def handle_success(self, result):
        node_version = result.get("nodeVersion", "Unknown node.js version")
        npm_version = result.get("npmVersion", "Unknown npm version")
        npx_version = result.get("npxVersion", "Unknown npx version")
        already_installed = result.get("alreadyInstalled", False)

        msg = "Node.js installed successfully"
        if already_installed:
            msg = "Node.js already installed"

        print(msg, node_version, npm_version, npx_version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Node Version: {node_version},,CHECKMARK|NPM Version: {npm_version},,CHECKMARK|NPX Version: {npx_version},,CHECKMARK")
