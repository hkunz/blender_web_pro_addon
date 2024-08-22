import os

from blender_web_pro.operators.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore

class WEB_OT_OperatorTestWebExport(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_website_export_operator"
    bl_label = "Test Web Export"
    bl_description = "Export project and test in default browser"
    bl_options = {'REGISTER'}

    @classmethod
    def get_web_file(cls):
        return "src/index.html"

    @classmethod
    def poll(cls, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        path = os.path.join(directory, cls.get_web_file())
        return os.path.isfile(path)
    