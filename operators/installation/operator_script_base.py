import subprocess
import requests
import json
import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup # type: ignore

class OperatorScriptBase(bpy.types.Operator):
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

    def execute_script(self, context):
        script_path = self.get_script_path()
        script_args = self.get_script_args()
        output = self.run_script(script_path, *script_args)
        if output is None:
            return
        print("Raw output to convert to json =======\n", output)
        result = self.get_json(output)
        print("Converted json result:\n", result)
        self.handle_success(result, context)
        cmd_output = result.get("commandOutput", [])
        self.report_command_output(cmd_output)

    def report_command_output(self, output_list):
        for output in output_list:
            output_str = str(output)
            lines = output_str.split('\n')
            for line in lines:
                if line.strip():  # Optional: Skip empty lines
                    self.report({'INFO'}, line)

    def handle_error(self, stdout, errorCode):
        result = self.get_json(stdout)
        error = result.get("error", "Unknown error")
        exception = result.get("exception", None)
        exception_full = result.get("exception_full", None)
        message = f"Script execution failed with code {str(errorCode)},,CANCEL,,1|{error},,CANCEL,,1"
        if exception:
            message += f"|{exception},,CANCEL,,1"
        create_generic_popup(message=message)
        self.report({'ERROR'}, f"{exception_full if exception_full else (exception if exception else error)}")

    def handle_unknown_error(self, e):
        self.report({'ERROR'}, str(e))
        create_generic_popup(message=f"Script execution failed with error code {str(e.returncode)},,CANCEL,,1|{e},,CANCEL,,1")

    def handle_success(self, _):
        raise NotImplementedError("Subclasses must implement this method")

    def execute(self, context):
        if self.check_internet():
            #FIXME: https://blender.stackexchange.com/questions/322779/how-can-i-get-info-report-to-show-up-before-subprocess-call
            #context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Installation in progress... Please wait."), title="Info", icon='INFO')
            #context.view_layer.update()
            #bpy.app.timers.register(self.execute_script, first_interval=0.1)
            self.execute_script(context)
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
