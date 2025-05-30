import bpy
import bpy_types
from typing import List

class OperatorGenericPopup(bpy.types.Operator):
    bl_idname = "wm.blender_web_pro_generic_popup"
    bl_label = "Blender Web Pro Message"
    bl_description = "Generic Popup Operator for displaying a custom message"
    bl_options = {'INTERNAL'}

    message: bpy.props.StringProperty(name="Message", default="") # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770
    exec_message: str = None
    width: int = 0

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        return True

    def invoke(self, context: bpy_types.Context, _: bpy.types.Event) -> set[str]:
        # return self.execute(context) # use this return statement if you want to skip the prompt and directly proceed to execution
        return context.window_manager.invoke_props_dialog(self, width=self.width) if self.width else context.window_manager.invoke_props_dialog(self)

    def draw(self, _: bpy_types.Context) -> None:
        layout: bpy.types.UILayout = self.layout
        col: bpy.types.UILayout = layout.box().column()
        list: List = self.message.split('|')
        for m in list:
            ico_msg=m.split(',,')
            if len(ico_msg) > 1:
                col.alert = len(ico_msg) > 2 and int(ico_msg[2])
                col.label(text=ico_msg[0], icon=ico_msg[1])
            else:
                col.label(text=m)

    def execute(self, _: bpy_types.Context) -> set[str]:
        if self.exec_message:
            self.report({'INFO'}, self.exec_message)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(OperatorGenericPopup)

def unregister() -> None:
    bpy.utils.unregister_class(OperatorGenericPopup)

def create_generic_popup(message: str) -> None:
    bpy.ops.wm.blender_web_pro_generic_popup('INVOKE_DEFAULT', message=message) # type: ignore
