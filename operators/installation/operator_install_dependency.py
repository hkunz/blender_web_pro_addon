import bpy
import bpy_types
import os
import shutil

from blender_web_pro.operators.installation.operator_script_base import OperatorScriptBase # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.utils.package_json import PackageJson # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore
from blender_web_pro.utils.ui_utils import UiUtils # type: ignore

class WEB_OT_OperatorInstallDependency(OperatorScriptBase):
    bl_options = {'INTERNAL'}

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        if not self.check_valid_directory():
            return {'CANCELLED'}
        return super().invoke(context, event)

    def check_valid_directory(self):
        props = bpy.context.scene.userinterface_props
        directory = props.output_directory.strip()
        if not os.path.isdir(directory):
            msg = "No directory path set. Please specify a valid directory." if not directory else "The provided path is not a valid directory"
            create_generic_popup(message=f"{msg},,CANCEL,,1")
            return False
        return True

    def generate_config_files(self, context):
        props: UserInterfacePropertyGroup = context.scene.userinterface_props
        directory = props.output_directory.strip()
        v = FileUtils.copy_template_file(directory, "vite.config.template.mjs")
        if not (os.path.exists(v)):
            self.report({'ERROR'}, f"One of the config files/directories could not be generated: \n\t{v}")
            return False
        return True

    def execute_script(self, context):
        copy_success = self.generate_config_files(context)
        if not copy_success:
            return
        super().execute_script(context)

    def handle_success(self, result, context):
        directory = result.get("directoryPath", "Unknown directory path")
        PackageJson().set_directory(directory, True)
        UiUtils.update_ui(context)
