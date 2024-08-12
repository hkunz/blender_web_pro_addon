import bpy

from typing import List, Tuple
from bpy.app.handlers import persistent

from blender_web_pro.operators.operator_empty import OBJECT_OT_OperatorEmpty # type: ignore
from blender_web_pro.operators.file.operator_file_vox_exporter import EXPORT_OT_file_vox # type: ignore
from blender_web_pro.operators.cache.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from blender_web_pro.operators.cache.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from blender_web_pro.operators.operator_test_web import WEB_OT_OperatorTestWeb # type: ignore
from blender_web_pro.operators.installation.operator_install_check import WEB_OT_OperatorInstallCheck # type: ignore
from blender_web_pro.operators.installation.operator_install_choco import WEB_OT_OperatorInstallChoco # type: ignore
from blender_web_pro.operators.installation.operator_install_nodejs_choco import WEB_OT_OperatorInstallNodeJS # type: ignore
from blender_web_pro.operators.installation.operator_install_nvm import WEB_OT_OperatorInstallNVM # type: ignore
from blender_web_pro.operators.installation.operator_install_threejs import WEB_OT_OperatorInstallThreeJS # type: ignore
from blender_web_pro.operators.installation.operator_install_vite_dependency import WEB_OT_OperatorInstallViteDependency # type: ignore
from blender_web_pro.ui.property_groups.property_group_installation_properties import InstallationPropertyGroup # type: ignore
from blender_web_pro.ui.property_groups.property_group_userinterface_properties import UserInterfacePropertyGroup # type: ignore
from blender_web_pro.utils.utils import Utils # type: ignore
from blender_web_pro.utils.object_utils import ObjectUtils # type: ignore
from blender_web_pro.utils.icons_manager import IconsManager  # type: ignore
from blender_web_pro.utils.package_json import PackageJson # type: ignore

IDNAME_ICONS = {
    "NodeSocketMaterial": "MATERIAL_DATA",
    "NodeSocketCollection": "OUTLINER_COLLECTION",
    "NodeSocketTexture": "TEXTURE_DATA",
    "NodeSocketImage": "IMAGE_DATA",
}
IDNAME_TYPE = {
    "NodeSocketMaterial": "materials",
    "NodeSocketCollection": "collections",
    "NodeSocketTexture": "textures",
    "NodeSocketImage": "images",
}

@persistent
def on_depsgraph_update(scene, depsgraph=None):
    context = bpy.context
    if not hasattr(context, "active_object"): # context is different when baking image
        return
    obj = context.active_object
    if not obj:
        return
    properties: UserInterfacePropertyGroup = context.scene.userinterface_props
    check_object_selection_change(context, properties, obj)

def my_sample_update_rgb_nodes(self, context):
    mat = self.id_data
    nodes = [n for n in mat.node_tree.nodes if isinstance(n, bpy.types.ShaderNodeRGB)]
    for n in nodes:
        n.outputs[0].default_value = self.rgb_controller

def check_object_selection_change(context, properties, obj):
    # if PREVIOUS_ACTIVE_OBJECT == obj:
    #     return
    # PREVIOUS_ACTIVE_OBJECT = obj
    pass

class MyPropertyGroup2(bpy.types.PropertyGroup):
    rgb_controller: bpy.props.FloatVectorProperty(
        name="Diffuse color",
        subtype='COLOR',
        default=(1, 1, 1, 1),
        size=4,
        min=0, max=1,
        description="color picker",
        update = my_sample_update_rgb_nodes
    ) # type: ignore

class OBJECT_PT_my_addon_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_my_addon_panel"
    bl_label = f"Blender Web Pro {Utils.get_addon_version()}"
    #use these 3 lines if you want the addon to be under a tab within N-Panel
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blender Web Pro'
    #use these 3 lines if you want the addon to be a custom tab under Object Properties
    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "object"

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        props = context.scene.installation_props
        if props.check_installation:
            layout.operator(WEB_OT_OperatorInstallCheck.bl_idname, text="Check Installation")
            return

        complete_installation = \
            props.installation_status_choco == InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED and \
            props.installation_status_nodejs == InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED and \
            props.installation_status_nvm == InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED

        self.draw_expanded_installation(context, layout, complete_installation)

        if not complete_installation:
            return

        self.draw_sample_expanded_options(context, layout)
        #self.draw_sample_color_picker(context, layout)
        #self.draw_sample_modifier_exposed_props(context, layout, "GeometryNodes")

    def draw_sample_modifier_exposed_props(self, context, layout, md_name = "GeometryNodes"):
        # to test this function add a Geometry Nodes Modifier by the name "GeometryNodes" and add some inputs to it which will get exposed in the addon panel
        # https://blender.stackexchange.com/questions/317739/unable-to-access-exposed-material-input-in-addon-from-geometry-nodes-modifier
        ob = context.object
        if not hasattr(ob, "modifiers") or md_name not in ob.modifiers:
            return
        md = ob.modifiers[md_name]
        if md.type == "NODES" and md.node_group:
            for rna in md.node_group.interface.items_tree:
                if hasattr(rna, "in_out") and rna.in_out == "INPUT":
                    self.add_layout_gn_prop_pointer(layout, md, rna)

    def draw_expanded_installation(self, context, layout, complete_installation):
        props = context.scene.installation_props
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_installation",
            icon=IconsManager.BUILTIN_ICON_DOWN if context.scene.expanded_installation else IconsManager.BUILTIN_ICON_RIGHT,
            icon_only=True, emboss=False
        )
        row.label(text="Installation")
        if context.scene.expanded_installation:
            properties: UserInterfacePropertyGroup = context.scene.userinterface_props
            col = layout.box().column()
            self.create_install_button(col, WEB_OT_OperatorInstallChoco.bl_idname, text="Chocolatey", state=props.installation_status_choco, version=props.installed_choco_v)
            self.create_install_button(col, WEB_OT_OperatorInstallNodeJS.bl_idname, text="Node.js", state=props.installation_status_nodejs, version=props.installed_nodejs_v)
            self.create_install_button(col, WEB_OT_OperatorInstallNVM.bl_idname, text="NVM", state=props.installation_status_nvm, version=props.installed_nvm_v)

            if not complete_installation:
                return

            box = layout.box().column()
            #box.label(text="Project Directory", icon="FILEBROWSER")
            box.prop(properties, "output_directory")
            props: UserInterfacePropertyGroup = context.scene.userinterface_props
            package_json = PackageJson()
            threejs_version = package_json.get_threejs_version()
            vite_version = package_json.get_vite_version()
            package_json.set_directory(props.output_directory)
            self.create_install_button(box, WEB_OT_OperatorInstallThreeJS.bl_idname, text="Three.js", state=bool(threejs_version), version=threejs_version)
            self.create_install_button(box, WEB_OT_OperatorInstallViteDependency.bl_idname, text="Vite", state=bool(vite_version), version=vite_version)
            #col.prop(data=context.scene.render,property="fps",text="Frame Rate 2") # https://blender.stackexchange.com/questions/317553/how-to-exposure-render-settings-to-addon-panel/317565#317565
            #self.add_layout_gn_prop(layout, context.object.modifiers["Geometry Nodes"], "Socket_2") # https://blender.stackexchange.com/questions/317571/how-can-i-expose-geometry-nodes-properties-in-my-addon-panel/317586
            #col.operator(EXPORT_OT_file_vox.bl_idname, text="Export Button")
            #col.operator(WEB_OT_OperatorTestWeb.bl_idname, text="Test Web")

    def create_install_dep_button(self, layout, operator, text, version):
        row = layout.row(align=True)
        text = "Install " + text if not version else text + " (" + version + ")"
        row.operator(operator, text=text)

    def create_install_button(self, layout, operator, text, state=0, version=""):
        row = layout.row(align=True)
        if state == InstallationPropertyGroup.INSTALLATION_STATUS_NOT_INSTALLED:
            row.label(text="", icon="IMPORT") #icon_value=IconsManager().get_icon_id(IconsManager.ICON_CHECKMARK))
        elif state == InstallationPropertyGroup.INSTALLATION_STATUS_INSTALLED:
            row.label(text="", icon="SEQUENCE_COLOR_04")
        elif state == InstallationPropertyGroup.INSTALLATION_STATUS_ERROR:
            row.label(text="", icon="CANCEL")
        else:
            row.label(text="", icon="ERROR")
        text = "Install " + text if not version else text + " (" + version + ")"
        row.operator(operator, text=text)

    def draw_sample_expanded_options(self, context, layout):
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_options",
            icon=IconsManager.BUILTIN_ICON_DOWN if context.scene.expanded_options else IconsManager.BUILTIN_ICON_RIGHT,
            icon_only=True, emboss=False
        )
        row.label(text="Export")
        if context.scene.expanded_options:
            col = layout.column()
            col.prop(data=context.scene.render,property="fps",text="Frame Rate") # https://blender.stackexchange.com/questions/317553/how-to-exposure-render-settings-to-addon-panel/317565#317565
            #self.add_layout_gn_prop(layout, context.object.modifiers["Geometry Nodes"], "Socket_2") # https://blender.stackexchange.com/questions/317571/how-can-i-expose-geometry-nodes-properties-in-my-addon-panel/317586
            col.operator(EXPORT_OT_file_vox.bl_idname, text="Export Button")
            col.operator(WEB_OT_OperatorTestWeb.bl_idname, text="Test Web")

    def draw_sample_color_picker(self, context, layout):
        ob = context.object
        if not ob: return
        mat = ob.active_material
        layout.prop(mat.my_slot_setting, "rgb_controller")
        # sample to set the color via python:
        # ob.active_material.slot_setting.rgb_controller = (1, 0, 0, 1)

    def add_layout_gn_prop(self, layout, modifier, prop_id):
        name = ObjectUtils.get_modifier_prop_name(modifier, prop_id)
        layout.prop(data=modifier, property=f'["{prop_id}"]', text=name)

    def add_layout_gn_prop_pointer(self, layout, md, rna): # Need to ensure that md and identifier are correct
        if rna.bl_socket_idname == "NodeSocketGeometry":
            return
        if rna.bl_socket_idname in IDNAME_ICONS:
            layout.prop_search(md, f'["{rna.identifier}"]',
                search_data = bpy.data,
                search_property = IDNAME_TYPE[rna.bl_socket_idname],
                icon = IDNAME_ICONS[rna.bl_socket_idname],
                text = "My " + rna.name
            )
        else:
            layout.prop(md, f'["{rna.identifier}"]', text=rna.name)

    @classmethod
    def poll(cls, context):
        return True

def register() -> None:
    bpy.utils.register_class(OBJECT_PT_my_addon_panel)
    bpy.utils.register_class(UserInterfacePropertyGroup)
    bpy.utils.register_class(MyPropertyGroup2)
    bpy.utils.register_class(InstallationPropertyGroup)
    bpy.utils.register_class(WEB_OT_OperatorInstallCheck)
    bpy.utils.register_class(WEB_OT_OperatorInstallChoco)
    bpy.utils.register_class(WEB_OT_OperatorInstallNodeJS)
    bpy.utils.register_class(WEB_OT_OperatorInstallNVM)
    bpy.utils.register_class(WEB_OT_OperatorInstallThreeJS)
    bpy.utils.register_class(WEB_OT_OperatorInstallViteDependency)
    bpy.utils.register_class(WEB_OT_OperatorTestWeb)
    bpy.types.Material.my_slot_setting = bpy.props.PointerProperty(type=MyPropertyGroup2)
    bpy.types.Scene.userinterface_props = bpy.props.PointerProperty(type=UserInterfacePropertyGroup)
    bpy.types.Scene.installation_props = bpy.props.PointerProperty(type=InstallationPropertyGroup)
    bpy.types.Scene.expanded_installation = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.expanded_options = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.register_class(EXPORT_OT_file_vox) # sample file export operator resulting in open dialog
    register_temp_cache_operator()
    register_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_PT_my_addon_panel)
    bpy.utils.unregister_class(UserInterfacePropertyGroup)
    bpy.utils.unregister_class(InstallationPropertyGroup)
    bpy.utils.unregister_class(MyPropertyGroup2)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallCheck)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallChoco)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallNodeJS)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallNVM)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallThreeJS)
    bpy.utils.unregister_class(WEB_OT_OperatorInstallViteDependency)
    bpy.utils.unregister_class(WEB_OT_OperatorTestWeb)
    del bpy.types.Material.my_slot_setting
    del bpy.types.Scene.expanded_installation
    del bpy.types.Scene.expanded_options
    del bpy.types.Scene.userinterface_props
    del bpy.types.Scene.installation_props
    bpy.utils.unregister_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.unregister_class(EXPORT_OT_file_vox)
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.clear()