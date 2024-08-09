import bpy
import bpy_types

from blender_web_pro.utils.temp_file_manager import TempFileManager # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import OperatorGenericPopup # type: ignore

class FILE_OT_ClearAllTempCacheOperator(OperatorGenericPopup):
    bl_idname = "file.blender_web_pro_clear_all_temp_cache"
    bl_label = "Clear All Blender Web Pro Cache"
    bl_description = "Delete all temporary Blender Web Pro cache directories regardless of Blender or addon versions"
    bl_options = {'REGISTER'}

    def draw(self, context: bpy_types.Context) -> None:
        self.message = "Delete all temporary Blender Web Pro directories?"
        self.exec_message = "Deleted all temporary Blender Web Pro directories"
        super().draw(context)

    def execute(self, context:bpy_types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        super().execute(context)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearAllTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearAllTempCacheOperator)