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

    def run_script(self, context, script_path, *args):
        try:
            command = ["powershell", "-File", script_path] + list(args)
            subprocess_result = subprocess.run(command, capture_output=False, text=True, check=True)
            self.on_script_exit_success(context)
            return True
        except subprocess.CalledProcessError as e:
            if e.returncode >= 10:
                self.on_script_exit_error(e.stdout, e.returncode)
            else:
                self.on_script_exit_unknown(e)
        except Exception as e:
            msg = f"Unknown error occured while running subprocess"
            self.report(msg)
            create_generic_popup(message=f"{msg},,CANCEL,,1")
        return False

    def get_json(self, raw):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error decoding json content: {raw}")
            self.report({'ERROR'}, f"JSON decode error: {e} ==== {raw}")
            create_generic_popup(message=f"Script execution failed,,CANCEL,,1|Invalid JSON output,,TRIA_RIGHT")
        return json.loads("{}")

    def get_logs_json(self):
        file = self.get_log_file()
        msg = None
        try:
            with open(file, 'r') as f:
                content = f.read()
                if content:
                    return self.get_json(content)
            msg = f"Log file is empty:"
        except FileNotFoundError:
            msg = f"Log file not found:"
        except IOError:
            msg = f"Error reading log file:"
        create_generic_popup(message=f"{msg},,CANCEL,,1|{file},,TRIA_RIGHT")
        self.report({'ERROR'}, f"{msg} {file}")
        return None

    def execute_script(self, context):
        script_path = self.get_script_path()
        script_args = self.get_script_args()
        success = self.run_script(context, script_path, *script_args)
        return success

    def report_command_output(self, output_list):
        for output in output_list:
            output_str = str(output)
            lines = output_str.split(OperatorScriptBase.LINE_END)
            for line in lines:
                if line.strip():  # Optional: Skip empty lines
                    self.report({'INFO'}, line)

    def on_script_exit_success(self, context):
        result = self.get_logs_json()
        if not result:
            return False
        self.handle_success(result, context)
        cmd_output = result.get("infos", [])
        self.report_command_output(cmd_output)
        UiUtils.update_ui(context)

    def on_script_exit_error(self, stdout, errorCode):
        result = self.get_logs_json()
        if not result:
            return False
        error = result.get("error", "Unknown error")
        errors = result.get("errors")
        exception = result.get("exception", None)
        exception_full = result.get("exception_full", None)
        message = f"Script execution failed with code {str(errorCode)},,CANCEL,,1|{error},,TRIA_RIGHT"
        if exception:
            message += f"|{exception},,TRIA_RIGHT"
        create_generic_popup(message=message)
        msg = exception_full if exception_full else (exception if exception else error)
        msg = "".join(msg).replace(OperatorScriptBase.LINE_END, OperatorScriptBase.NEW_LINE)
        if not errors:
            self.report({'ERROR'}, f"{msg}")
            return
        for err in errors:
            self.report({'ERROR'}, f"{err}")

    def on_script_exit_unknown(self, e):
        self.report({'ERROR'}, str(e))
        create_generic_popup(message=f"Unknown script exit error,,CANCEL|Script exit with error code {str(e.returncode)},,TRIA_RIGHT")

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
