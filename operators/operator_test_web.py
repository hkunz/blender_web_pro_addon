from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore

class WEB_OT_OperatorTestWeb(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_website_operator"
    bl_label = "Test WebGL Three.js"
    bl_description = "Starts the Vite Server to host the website, which opens the site in your default web browser for testing."
    bl_options = {'REGISTER'}

    def get_web_file(self):
        return "test.html"
