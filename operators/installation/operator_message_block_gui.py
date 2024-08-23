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
    def lock_UI(cls, except_window=None):
        cls._finish_request = False

        for window in bpy.context.window_manager.windows:
            if window is except_window:
                continue
            if window not in cls._active_modals:
                with bpy.context.temp_override(window=window):
                    bpy.ops.wm.blocking()

    @classmethod
    def unlock_UI(cls):
        cls._finish_request = True
        cls._active_modals.clear()

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
        self.is_multi_window = len(context.window_manager.windows) != 1
        if self.is_multi_window:
            BlockUI.lock_UI(except_window=context.window)

        command = ["powershell", "-Command", "Start-Sleep -Seconds 5; Write-Output 'Completed long-running task'"]
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # need catch here because when your code raise error,
        # operartor will dead and unlock_UI will never run, and the sub-window will lock forever.
        
        # Another problem is: you need add a modal timer to keep the modal running,
        # Otherwise, the modal will not run when the mouse is not moving or no keyboard events.
        try:
            if self.process.poll() is not None:
                output, error = self.process.communicate()
                print("Command output:", output)
                print("Command error:", error)
                BlockUI.unlock_UI()
                return {'FINISHED'}
        except:
            BlockUI.unlock_UI()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

classes = (
    BlockUI,
    SimpleOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

if __name__ == "__main__":
    register()