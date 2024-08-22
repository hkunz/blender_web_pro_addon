import os
import shutil

from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.operator_test_web_base import WEB_OT_OperatorTestWebBase # type: ignore
from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorTestWeb(WEB_OT_OperatorTestWebBase):
    bl_idname = "blender_web_pro.test_website_operator"
    bl_label = "Test WebGL Three.js"
    bl_description = "Starts the Vite Server to host the website, which opens the site in your default web browser for testing."
    bl_options = {'REGISTER'}

    def check_required_files_exist(self, directory, test=True):
        m = os.path.join(directory, "dist/src/models/")
        t = os.path.join(directory, "dist/src/textures/")
        os.makedirs(m, exist_ok=True)
        os.makedirs(t, exist_ok=True)
        src = os.path.join(FileUtils.get_addon_root_dir(), "resources/templates/project-template/dist/src/models/metal-cube.glb")
        shutil.copy(src, m)
        src = os.path.join(FileUtils.get_addon_root_dir(), "resources/templates/project-template/dist/src/textures/kloofendal_48d_partly_cloudy_puresky_1k.hdr")
        shutil.copy(src, t)
        return super().check_required_files_exist(directory, test)

    @classmethod
    def get_web_file(cls):
        return "test.html"
