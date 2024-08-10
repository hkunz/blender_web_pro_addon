import subprocess
import requests
import json
import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore

class OperatorInstallBase(bpy.types.Operator):
    bl_options = {'INTERNAL'}

    def get_script_path(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_script_args(self):
        return []  # Override in subclasses to provide arguments

    def run_script(self, script_path, *args):
        try:
            command = ["powershell", "-File", script_path] + list(args)
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if e.returncode >= 10:
                self.handle_error(e.stdout, e.returncode)
            else:
                self.handle_unknown_error(e)
        return None

    def get_json(self, raw):
        try:
            result = json.loads(raw)
            return result
        except json.JSONDecodeError as e:
            self.report({'ERROR'}, f"JSON decode error: {e}")
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|Invalid JSON output,,CANCEL,,1")
        return None

    def execute_script(self):
        script_path = self.get_script_path()
        script_args = self.get_script_args()
        output = self.run_script(script_path, *script_args)
        if output is None:
            return
        result = self.get_json(output)
        self.handle_success(result)
        output = result.get("commandOutput", "")
        output = '\n'.join(output)
        self.report({'INFO'}, f"{output}")

    def handle_error(self, stdout, errorCode):
        result = self.get_json(stdout)
        error = result.get("error", "Unknown error")
        exception = result.get("exception", "No additional information")
        exception_full = result.get("exception_full", "No additional information")
        self.report({'ERROR'}, f"{exception_full}")
        create_generic_popup(message=f"Script execution failed with code {str(errorCode)},,CANCEL,,1|{error},,CANCEL,,1|{exception},,CANCEL,,1")

    def handle_unknown_error(self, e):
        self.report({'ERROR'}, str(e))
        create_generic_popup(message=f"Script execution failed with error code {str(e.returncode)},,CANCEL,,1|{e},,CANCEL,,1")

    def handle_success(self, _):
        raise NotImplementedError("Subclasses must implement this method")

    def execute(self, context):
        if self.check_internet():
            self.execute_script()
        else:
            self.report({'ERROR'}, f"No internet connection. Please check your internet connection!")
        return {'FINISHED'}

    def check_internet(self, url='http://www.google.com', timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    @classmethod
    def poll(cls, context):
        return True
