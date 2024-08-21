# Alternate solution for https://blender.stackexchange.com/questions/322779/how-can-i-get-info-report-to-show-up-before-subprocess-call
# But this solution is not perfect yet

import bpy
import subprocess

class BlockUI(bpy.types.Operator):
    bl_idname = "wm.blocking"
    bl_label = "Blocking Modal"
    bl_options = {"INTERNAL"}

    _finish_request = False
    _active_modals = {}

    def execute(self, context):
        BlockUI._finish_request = False
        BlockUI._active_modals.clear()

        context.window_manager.modal_handler_add(self)
        BlockUI._active_modals[context.window] = self
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if BlockUI._finish_request:
            BlockUI._active_modals.pop(context.window, None)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    @classmethod
    def lock_UI(cls):
        cls._finish_request = False

        for window in bpy.context.window_manager.windows:
            if window not in cls._active_modals:
                with bpy.context.temp_override(window=window):
                    bpy.ops.wm.blocking()

    @classmethod
    def unlock_UI(cls):
        cls._finish_request = True
        cls._active_modals.clear()


# Usage:

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Operator"

    process = None

    def execute(self, context):
        context.window_manager.popup_menu(
            lambda self, context: self.layout.label(text="Installation in progress... Please wait. Interface will lock."),
            title="Info",
            icon='INFO'
        )
        BlockUI.lock_UI()
        command = ["powershell", "-Command", "Start-Sleep -Seconds 5; Write-Output 'Completed long-running task'"]
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if self.process.poll() is not None:
            output, error = self.process.communicate()
            print("Command output:", output)
            print("Command error:", error)
            BlockUI.unlock_UI()
            return {'FINISHED'}

        return {'PASS_THROUGH'}

classes = (
    BlockUI,
    SimpleOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

if __name__ == "__main__":
    register()
