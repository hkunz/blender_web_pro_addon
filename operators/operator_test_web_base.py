import bpy
import subprocess
import os
import time
import re

from blender_web_pro.utils.file_utils import FileUtils # type: ignore
from blender_web_pro.utils.package_json import PackageJson # type: ignore
from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore
from blender_web_pro.enums.debug_enum import DebugEnum # type: ignore

class WEB_OT_OperatorTestWebBase(bpy.types.Operator):
    bl_idname = "blender_web_pro.test_website_operator"
    bl_label = "Test WebGL Three.js"
    bl_description = "Starts the Vite Server to host the website, which opens the site in your default web browser for testing."
    bl_options = {'INTERNAL'}

    def sleepy(self):
        time.sleep(5)

    def start_vite_server(self, context, directory):
        server_script = os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/', r'start-vite-server.py')
        context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Web page will open... Please wait."), title="Info", icon='INFO')
        subprocess.Popen(['python', server_script, directory])
        bpy.app.timers.register(self.sleepy, first_interval=0.1)

    def get_vite_config_file(self, directory):
        return os.path.join(directory, "vite.config.mjs")

    @classmethod
    def get_web_file(cls):
        return "index.html"

    def get_public_dir(self):
        return "public/"

    def update_vite_config(self, directory):
        config = self.get_vite_config_file(directory)
        content = None
        with open(config, 'r') as file:
            content = file.read()
        pattern = r'(open:\s*)[^,\}\n]*'
        replacement = rf'\1"{self.get_web_file()}"'
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content == content:
            return
        with open(config, 'w') as file:
            file.write(new_content)
        print(f"Updated config file: {config}")

    def check_required_files_exist(self, directory, test=False):
        if not self.check_valid_vite_directory(directory):
            return False
        s = os.path.join(directory, self.get_web_file())
        p = os.path.join(directory, self.get_public_dir())
        t = FileUtils.copy_template_file(directory, "test.template.html", not DebugEnum.DEBUG_WEB_TEST_OVERWRITE, DebugEnum.DEBUG_USE_SYMLINK_COPY)
        if test and os.path.isfile(t):
            return True
        if not (os.path.isfile(t) and os.path.isdir(p) and os.path.isfile(s)):
            self.report({'ERROR'}, f"One of the required dir/files was not generated: \n\t{p}\n\t{s}\n\t{t}")
            return False
        return True

    def execute(self, context):
        props = context.scene.userinterface_props
        directory = props.output_directory.strip()
        check = self.check_required_files_exist(directory)
        if check:
            self.update_vite_config(directory)
            self.start_vite_server(context, directory)
        return {'FINISHED'}

    def check_valid_vite_directory(self, directory):
        if not os.path.isdir(directory):
            print(f"The path '{directory}' is not a valid directory.")
            create_generic_popup(message=f"The path is not a valid directory,,CANCEL,,1|'{directory}',,CANCEL,,1")
            return False
    
        package_json = PackageJson()
        package_json.set_directory(directory)
        package_json.check_dependencies()
        package_json.check_dev_dependencies()
        vite_version = package_json.get_vite_version()
        threejs_version = package_json.get_threejs_version()

        config_file_path = self.get_vite_config_file(directory)
        config_file = os.path.basename(config_file_path)
        config = os.path.isfile(config_file_path)

        if config and vite_version and threejs_version:
            print(f"Vite dependency ({vite_version}) and Three.js ({threejs_version}) has been configured in this directory since '{config_file}' exists in the directory '{directory}'.")
            return True

        message = f"Missing configuration for directory,,CANCEL,,1|'{directory}',,CANCEL,,1"

        if not config and vite_version:
            print(f"Missing {config_file} config file in directory")
            message += f"|Missing {config_file} config file in directory,,CANCEL,,1|Click \"Install Vite Dependency\" button,,CHECKMARK"

        if not threejs_version:
            print(f"No Three.js dependency configured for the directory")
            message += f"|No Three.js dependency configured for this directory,,CANCEL,,1|Click \"Install Three.js\" button,,CHECKMARK"

        if not vite_version:
            print(f"No vite dependency configured for the directory: '{directory}'")
            message += f"|No vite dependency configured for this directory,,CANCEL,,1|Click \"Install Vite Dependency\" button,,CHECKMARK"

        create_generic_popup(message=message)
        return False

    @classmethod
    def poll(cls, _context):
        return True
