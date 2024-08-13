import subprocess
import platform
import requests
import json
import bpy

from blender_web_pro.operators.common.operator_generic_popup import create_generic_popup, OperatorGenericPopup # type: ignore
from blender_web_pro.utils.ui_utils import UiUtils # type: ignore

class OperatorScriptBase(OperatorGenericPopup):
    bl_options = {'INTERNAL'}

    LINE_END = '{LINE_END}'
    NEW_LINE = '\n'

    def get_log_file(self):
        return NotImplementedError("Subclasses must implement this method")

    def get_script_path(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_script_args(self):
        return []  # Override in subclasses to provide arguments

    def run_script(self, script_path, *args):
        try:
            command = ["powershell", "-File", script_path] + list(args)
            result = subprocess.run(command, capture_output=False, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if e.returncode >= 10:
                self.handle_error(e.stdout, e.returncode)
            else:
                self.handle_unknown_error(e)
        return None

    def get_json(self, raw):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error decoding json content: {raw}")
            self.report({'ERROR'}, f"JSON decode error: {e} ==== {raw}")
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|Invalid JSON output,,CANCEL,,1")
        return json.loads("{}")

    def get_logs_json(self, file):
        try:
            with open(file, 'r') as file:
                raw_content = file.read()
                return self.get_json(raw_content)
        except FileNotFoundError:
            print(f"Log file not found: {file}")
            create_generic_popup(message=f"Log file not found,,CANCEL,,1|{file},,CANCEL,,1")
        except IOError:
            print(f"Error reading log file: {file}")
            create_generic_popup(message=f"Error reading log file,,CANCEL,,1|{file},,CANCEL,,1")
        return json.loads("{}")


    def execute_script(self, context):
        script_path = self.get_script_path()
        script_args = self.get_script_args()
        self.run_script(script_path, *script_args)
        log_file = self.get_log_file()
        result = self.get_logs_json(log_file)
        self.handle_success(result, context)
        if not result:
            print("\nERROR:\nThe raw json output is not pure json, please check that commands don't print to the console by using *>&1 | Out-String in the ps1 file")
            return
        cmd_output = result.get("commandOutput", [])
        self.report_command_output(cmd_output)
        UiUtils.update_ui(context)

    def report_command_output(self, output_list):
        for output in output_list:
            output_str = str(output)
            lines = output_str.split(OperatorScriptBase.LINE_END)
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
        msg = exception_full if exception_full else (exception if exception else error)
        msg = "".join(msg).replace(OperatorScriptBase.LINE_END, OperatorScriptBase.NEW_LINE)
        self.report({'ERROR'}, f"{msg}")

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
