import bpy
import bpy_types

from typing import List, Tuple

from blender_web_pro.enums.debug_enum import DebugEnum # type: ignore

def my_sample_settings_callback(self: bpy.types.Scene, context: bpy_types.Context) -> List[Tuple[str, str, str]]:
    SAMPLE_LIST: List[Tuple[str, str, str]] = [
        ("NONE", "None", "Item Description"),
        ("OPT1", "Option 1", "Item Description for Option 1"),
        ("OPT2", "Option 2", "Item Description for Option 2"),
    ]
    return SAMPLE_LIST

class UserInterfacePropertyGroup(bpy.types.PropertyGroup):

    output_directory: bpy.props.StringProperty(
        name="",
        description="Directory where to install Three.js",
        subtype='DIR_PATH',
        default=f"{DebugEnum.DEBUG_PROJECT_PATH}"
    ) # type: ignore

    my_enum_prop: bpy.props.EnumProperty(
        name="My Enum Prop",
        description="My enum prop description",
        items=my_sample_settings_callback,
        #default="NONE", # cannot set a default when using dynamic EnumProperty
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    my_float_prop: bpy.props.FloatProperty(
        name="My Float Prop",
        description="My float prop description",
        default=0,
        min=-10.0,
        max=10.0,
        precision=2,
        #update=on_float_input_change,
        #set=validate_input # does not work. so we can only update in on_input_voxelsize_change
    ) # type: ignore

    my_string_prop: bpy.props.StringProperty(
        name="My String Prop",
        description="My string prop description",
        #update=on_string_input_change
    ) # type: ignore

    my_file_input_prop: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    ) # type: ignore