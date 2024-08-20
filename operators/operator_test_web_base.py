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

    def start_vite_server(self, context):
        props = context.scene.userinterface_props
        directory = props.output_directory
        server_script = os.path.join(FileUtils.get_addon_root_dir(), r'utils/scripts/', r'start-vite-server.py')
        if not self.check_valid_vite_directory(directory):
            return
        context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Web page will open... Please wait."), title="Info", icon='INFO')
        subprocess.Popen(['python', server_script, directory])
        bpy.app.timers.register(self.sleepy, first_interval=0.1)

    def copy_template_files(self, context, skip_exists, symlink):
        props: UserInterfacePropertyGroup = context.scene.userinterface_props
        directory = props.output_directory.strip()
        t = FileUtils.copy_template_file(directory, "test.template.html", skip_exists, symlink)
        i = FileUtils.copy_template_file(directory, "index.template.html", skip_exists, symlink)
        m = FileUtils.copy_template_file(directory, "main.template.js", skip_exists, symlink)
        s = FileUtils.copy_template_file(directory, "styles.template.css", skip_exists, symlink)
        if not (os.path.exists(t) and os.path.exists(i) and os.path.exists(m) and os.path.exists(s)):
            self.report({'ERROR'}, f"One of the web files could not be generated: \n\t{t}\n\t{i}\n\t{m}\n\t{s}\n\t")
            return False
        return True

    def get_vite_config_file_path(self):
        props = bpy.context.scene.userinterface_props
        output_directory = props.output_directory.strip()
        return os.path.join(output_directory, "vite.config.mjs")

    def get_web_file(self):
        return "index.html"

    def update_vite_config(self):
        config = self.get_vite_config_file_path()
        if not os.path.isfile(config):
            return
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

    def execute(self, context):
        self.update_vite_config()
        copy_success = self.copy_template_files(context, not DebugEnum.DEBUG_WEB_TEST_OVERWRITE, DebugEnum.DEBUG_USE_SYMLINK_COPY)
        if copy_success:
            self.start_vite_server(context)
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

        config_file_path = self.get_vite_config_file_path()
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
