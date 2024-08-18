import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.utils.package_json import PackageJson # type: ignore
from blender_web_pro.utils.ui_utils import UiUtils # type: ignore

class BWP_OT_OperatorClearPackageJsonCache(bpy.types.Operator):
    bl_idname = "blender_web_pro.clear_package_json_cache"
    bl_label = "Clear package.json Cache"
    bl_description = "Clear the cache of loaded content data from package.json files contained in each visited directory"
    bl_options = {'REGISTER'}

    def execute(self, context):
        PackageJson().clear_cache_all()
        UiUtils.update_ui(context)
        self.report({'INFO'}, "Cleared package.json Cache")
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True
