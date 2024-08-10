import subprocess
import json
import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore

class OperatorInstallBase(bpy.types.Operator):
    bl_options = {'INTERNAL'}

    def get_script_path(self):
        raise NotImplementedError("Subclasses must implement this method")

    def run_script(self, script_path):
        try:
            result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, e)
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|{e},,CANCEL,,1")
            return None

    def execute_script(self):
        script_path = self.get_script_path()
        output = self.run_script(script_path)
        if output is None:
            return

        try:
            result = json.loads(output)
        except json.JSONDecodeError as e:
            self.report({'ERROR'}, f"JSON decode error: {e}")
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|Invalid JSON output,,CANCEL,,1")
            return

        if not result.get("success", False):
            error = result.get("error", "Unknown error")
            exception = result.get("exception", "No additional information")
            exception_full = result.get("exception_full", "No additional information")
            self.report({'ERROR'}, f"{exception_full}")
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|{error},,CANCEL,,1|{exception},,CANCEL,,1")
            return

        self.handle_success(result)
        output = result.get("commandOutput", "")
        output = '\n'.join(output)
        self.report({'INFO'}, f"{output}")

    def handle_success(self, result):
        raise NotImplementedError("Subclasses must implement this method")

    def execute(self, context):
        self.execute_script()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True
