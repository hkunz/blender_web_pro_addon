import subprocess
import os
import bpy

from blender_web_pro.utils.file_utils import FileUtils # type: ignore

class WEB_OT_OperatorTestWeb(bpy.types.Operator):
    bl_idname = "web.blender_web_pro_test_web_operator"
    bl_label = "Test Web"
    bl_description = "Test Web Button using Vite Server which opens a tab in your default browser"
    bl_options = {'REGISTER'}

    def start_vite_server(self):
        directory = r'C:\Users\harry\workspace\test' # testing TODO
        #bpy.ops.wm.console_toggle()
        server_script = os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/', r'start-vite-server.py')
        subprocess.Popen(['python', server_script, directory])

    def execute(self, _context):
        self.start_vite_server()
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return True
