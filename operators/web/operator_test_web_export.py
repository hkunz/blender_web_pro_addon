import os

from blender_web_pro.operators.web.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore

class WEB_OT_OperatorTestWebExport(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_project"
    bl_label = "Test Project"
    bl_description = "Export project and test in default browser"
    bl_options = {'REGISTER'}

    def get_wait_open_message(self):
        return "The project webpage is opening... Please wait."

    @classmethod
    def get_web_file(cls):
        return "src/index.html"

    @classmethod
    def poll(cls, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        path = os.path.join(directory, cls.get_web_file())
        return os.path.isfile(path)