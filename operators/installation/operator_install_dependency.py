import bpy
import os
import shutil

from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.utils.package_json import PackageJson # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorInstallDependency(OperatorScriptBase):
    bl_options = {'INTERNAL'}

    def execute_script(self, context):
        super().execute_script(context)
        props: UserInterfacePropertyGroup = context.scene.userinterface_props
        directory = props.output_directory
        public_directory = os.path.join(directory, "public")
        if not os.path.exists(public_directory):
            os.makedirs(public_directory)
        self.copy_template_file(directory, "vite.config.mjs")
        self.copy_template_file(directory, "index.html")
        self.copy_template_file(directory, "main.js")

    def copy_template_file(self, directory, file):
        tgt = os.path.join(directory, file)
        if os.path.isfile(tgt):
            print("Skip copy template file since it already exists: ", tgt)
            return
        src = os.path.join(FileUtils.get_addon_root_dir(), f'resources/templates/{file}.template')
        self.report({'INFO'}, f"Generated config file: {tgt}")
        shutil.copy(src, tgt)

    def handle_success(self, result, context):
        directory = result.get("directoryPath", "Unknown directory path")
        PackageJson().clear_cache(directory)