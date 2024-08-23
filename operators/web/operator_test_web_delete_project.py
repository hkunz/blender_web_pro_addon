import bpy
import os

from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.web.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore
from blender_web_pro.utils.ui_utils import UiUtils # type: ignore

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup, OperatorGenericPopup # type: ignore

class WEB_OT_OperatorTestWebDeleteProject(WEB_OT_OperatorTestWebBase, OperatorGenericPopup):
    bl_idname = "blender_web_pro.delete_project"
    bl_label = "Delete Project"
    bl_description = "Delete Project by removing Web Pro related directories that were created with 'Create Project' button"
    bl_options = {'REGISTER'}

    def draw(self, context) -> None:
        self.message = "Proceed deleting Project?|Only deletes files created with 'Create Project',,INFO"
        super().draw(context)

    def execute(self, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        FileUtils.delete_directory(os.path.join(directory, self.get_public_dir()))
        FileUtils.delete_directory(os.path.join(directory, "src"))
        FileUtils.delete_directory(os.path.join(directory, "dist"))
        msg = f"Deleted Project Files"
        create_generic_popup(message=f"{msg},,CHECKMARK")
        self.report({'INFO'}, msg)
        UiUtils.update_ui(context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True
