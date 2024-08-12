import os

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore

class WEB_OT_OperatorInstallNodeJS(OperatorScriptBase):
    bl_idname = "blender_web_pro.install_nodejs_operator"
    bl_label = "Install Node.js"
    bl_description = "Install Node.js which is a JavaScript runtime built on Chrome's V8 JavaScript engine"

    def draw(self, context) -> None:
        self.message = "Proceed with Node.js Installation?|Please wait while installation completes.,,INFO|This may take several minutes.,,INFO"
        self.exec_message = "Installing Node.js ... Please wait ..."
        super().draw(context)

    def get_script_path(self):
        return os.path.join(os.getcwd(), r'utils/scripts/windows', 'install-nodejs-choco.ps1')

    def handle_success(self, result, context):
        node_version = result.get("nodeVersion", "Unknown node.js version")
        npm_version = result.get("npmVersion", "Unknown npm version")
        npx_version = result.get("npxVersion", "Unknown npx version")
        already_installed = result.get("alreadyInstalled", False)

        msg = "Node.js is installed successfully"
        if already_installed:
            msg = "Node.js is already installed"

        props = context.scene.installation_props
        props.installation_status_nodejs = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_nodejs_v = node_version
        props.installation_status_npm = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_npm_v = npm_version
        props.installation_status_npx = InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED
        props.installed_npx_v = npx_version

        print(msg, node_version, npm_version, npx_version)
        create_generic_popup(message=f"{msg},,CHECKMARK|Node Version: {node_version},,CHECKMARK|NPM Version: {npm_version},,CHECKMARK|NPX Version: {npx_version},,CHECKMARK")

    @classmethod
    def poll(cls, context):
        props: InstallationPropertyGroup = context.scene.installation_props
        return props.installed_choco_v != ""
