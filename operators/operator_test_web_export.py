from blender_web_pro.operators.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore

class WEB_OT_OperatorTestWebExport(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_website_export_operator"
    bl_label = "Test Web Export"
    bl_description = "Export project and test in default browser"
    bl_options = {'REGISTER'}

    def get_web_file(self):
        return "src/index.html"
