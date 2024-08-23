import bpy
import os

from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.operators.web.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore
from blender_web_pro.utils.ui_utils import UiUtils # type: ignore

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup, OperatorGenericPopup # type: ignore

class WEB_OT_OperatorTestWebResetDirectory(OperatorGenericPopup):
    bl_idname = "blender_web_pro.reset_directory"
    bl_label = "Reset Directory"
    bl_description = "Delete everything in the selected directory"
    bl_options = {'REGISTER'}

    def draw(self, context) -> None:
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        self.message = f"Reset selected directory?,,ERROR,,1|Are you sure you want to delete directory contents?,,TRIA_RIGHT|{directory},,TRIA_RIGHT"
        super().draw(context)

    def execute(self, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        success = FileUtils.reset_directory(directory)
        if not success:
            create_generic_popup(message="Directory does not exist,,CANCEL")
            return {'CANCELLED'}
        msg = "Deleted Directory Contents"
        create_generic_popup(message=f"{msg},,CHECKMARK")
        self.report({'INFO'}, msg)
        UiUtils.update_ui(context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        return os.path.isdir(directory)
