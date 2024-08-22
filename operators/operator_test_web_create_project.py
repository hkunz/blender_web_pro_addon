import bpy
import os

from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorTestWebCreateProject(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_create_website_operator"
    bl_label = "Create Project"
    bl_description = "Create Project by copying template files into chosen directory"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        os.makedirs(os.path.join(directory, "public/"), exist_ok=True)
        src = os.path.join(FileUtils.get_addon_root_dir(), "resources/templates/project-template/")
        FileUtils.copy_dir_contents(src, directory, True)
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return True
