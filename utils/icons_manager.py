import bpy
import os
import bpy.utils.previews

from blender_web_pro.utils.file_utils import FileUtils # type: ignore


class IconsManager:

    _instance = None

    ICON_LIST=["NONE", "QUESTION", "ERROR", "CANCEL", "TRIA_RIGHT", "TRIA_DOWN", "TRIA_LEFT", "TRIA_UP", "ARROW_LEFTRIGHT", "PLUS", "DISCLOSURE_TRI_DOWN", "DISCLOSURE_TRI_RIGHT", "RADIOBUT_OFF", "RADIOBUT_ON", "MENU_PANEL", "BLENDER", "GRIP", "DOT", "COLLAPSEMENU", "X", "GO_LEFT", "PLUG", "UI", "NODE", "NODE_SEL", "FULLSCREEN", "SPLITSCREEN", "RIGHTARROW_THIN", "BORDERMOVE", "VIEWZOOM", "ZOOMIN", "ZOOMOUT", "PANEL_CLOSE", "COPY_ID", "EYEDROPPER", "LINK_AREA", "AUTO", "CHECKBOX_DEHLT", "CHECKBOX_HLT", "UNLOCKED", "LOCKED", "UNPINNED", "PINNED", "SCREEN_BACK", "RIGHTARROW", "DOWNARROW_HLT", "DOTSUP", "DOTSDOWN", "LINK", "INLINK", "PLUGIN", "HELP", "GHOST_ENABLED", "COLOR", "LINKED", "UNLINKED", "HAND", "ZOOM_ALL", "ZOOM_SELECTED", "ZOOM_PREVIOUS", "ZOOM_IN", "ZOOM_OUT", "RENDER_REGION", "BORDER_RECT", "BORDER_LASSO", "FREEZE", "STYLUS_PRESSURE", "GHOST_DISABLED", "NEW", "FILE_TICK", "QUIT", "URL", "RECOVER_LAST", "FULLSCREEN_ENTER", "FULLSCREEN_EXIT", "BLANK1", "LAMP", "MATERIAL", "TEXTURE", "ANIM", "WORLD", "SCENE", "EDIT", "GAME", "RADIO", "SCRIPT", "PARTICLES", "PHYSICS", "SPEAKER", "TEXTURE_SHADED", "VIEW3D", "IPO", "OOPS", "BUTS", "FILESEL", "IMAGE_COL", "INFO", "SEQUENCE", "TEXT", "IMASEL", "SOUND", "ACTION", "NLA", "SCRIPTWIN", "TIME", "NODETREE", "LOGIC", "CONSOLE", "PREFERENCES", "CLIP", "ASSET_MANAGER", "OBJECT_DATAMODE", "EDITMODE_HLT", "FACESEL_HLT", "VPAINT_HLT", "TPAINT_HLT", "WPAINT_HLT", "SCULPTMODE_HLT", "POSE_HLT", "PARTICLEMODE", "LIGHTPAINT", "SCENE_DATA", "RENDERLAYERS", "WORLD_DATA", "OBJECT_DATA", "MESH_DATA", "CURVE_DATA", "META_DATA", "LATTICE_DATA", "LAMP_DATA", "MATERIAL_DATA", "TEXTURE_DATA", "ANIM_DATA", "CAMERA_DATA", "PARTICLE_DATA", "LIBRARY_DATA_DIRECT", "GROUP", "ARMATURE_DATA", "POSE_DATA", "BONE_DATA", "CONSTRAINT", "SHAPEKEY_DATA", "CONSTRAINT_BONE", "CAMERA_STEREO", "PACKAGE", "UGLYPACKAGE", "BRUSH_DATA", "IMAGE_DATA", "FILE", "FCURVE", "FONT_DATA", "RENDER_RESULT", "SURFACE_DATA", "EMPTY_DATA", "SETTINGS", "RENDER_ANIMATION", "RENDER_STILL", "BOIDS", "STRANDS", "LIBRARY_DATA_INDIRECT", "GREASEPENCIL", "LINE_DATA", "GROUP_BONE", "GROUP_VERTEX", "GROUP_VCOL", "GROUP_UVS", "RNA", "RNA_ADD", "OUTLINER_OB_EMPTY", "OUTLINER_OB_MESH", "OUTLINER_OB_CURVE", "OUTLINER_OB_LATTICE", "OUTLINER_OB_META", "OUTLINER_OB_LAMP", "OUTLINER_OB_CAMERA", "OUTLINER_OB_ARMATURE", "OUTLINER_OB_FONT", "OUTLINER_OB_SURFACE", "OUTLINER_OB_SPEAKER", "RESTRICT_VIEW_OFF", "RESTRICT_VIEW_ON", "RESTRICT_SELECT_OFF", "RESTRICT_SELECT_ON", "RESTRICT_RENDER_OFF", "RESTRICT_RENDER_ON", "OUTLINER_DATA_EMPTY", "OUTLINER_DATA_MESH", "OUTLINER_DATA_CURVE", "OUTLINER_DATA_LATTICE", "OUTLINER_DATA_META", "OUTLINER_DATA_LAMP", "OUTLINER_DATA_CAMERA", "OUTLINER_DATA_ARMATURE", "OUTLINER_DATA_FONT", "OUTLINER_DATA_SURFACE", "OUTLINER_DATA_SPEAKER", "OUTLINER_DATA_POSE", "MESH_PLANE", "MESH_CUBE", "MESH_CIRCLE", "MESH_UVSPHERE", "MESH_ICOSPHERE", "MESH_GRID", "MESH_MONKEY", "MESH_CYLINDER", "MESH_TORUS", "MESH_CONE", "LAMP_POINT", "LAMP_SUN", "LAMP_SPOT", "LAMP_HEMI", "LAMP_AREA", "META_EMPTY", "META_PLANE", "META_CUBE", "META_BALL", "META_ELLIPSOID", "META_CAPSULE", "SURFACE_NCURVE", "SURFACE_NCIRCLE", "SURFACE_NSURFACE", "SURFACE_NCYLINDER", "SURFACE_NSPHERE", "SURFACE_NTORUS", "CURVE_BEZCURVE", "CURVE_BEZCIRCLE", "CURVE_NCURVE", "CURVE_NCIRCLE", "CURVE_PATH", "COLOR_RED", "COLOR_GREEN", "COLOR_BLUE", "FORCE_FORCE", "FORCE_WIND", "FORCE_VORTEX", "FORCE_MAGNETIC", "FORCE_HARMONIC", "FORCE_CHARGE", "FORCE_LENNARDJONES", "FORCE_TEXTURE", "FORCE_CURVE", "FORCE_BOID", "FORCE_TURBULENCE", "FORCE_DRAG", "FORCE_SMOKEFLOW", "MODIFIER", "MOD_WAVE", "MOD_BUILD", "MOD_DECIM", "MOD_MIRROR", "MOD_SOFT", "MOD_SUBSURF", "HOOK", "MOD_PHYSICS", "MOD_PARTICLES", "MOD_BOOLEAN", "MOD_EDGESPLIT", "MOD_ARRAY", "MOD_UVPROJECT", "MOD_DISPLACE", "MOD_CURVE", "MOD_LATTICE", "CONSTRAINT_DATA", "MOD_ARMATURE", "MOD_SHRINKWRAP", "MOD_CAST", "MOD_MESHDEFORM", "MOD_BEVEL", "MOD_SMOOTH", "MOD_SIMPLEDEFORM", "MOD_MASK", "MOD_CLOTH", "MOD_EXPLODE", "MOD_FLUIDSIM", "MOD_MULTIRES", "MOD_SMOKE", "MOD_SOLIDIFY", "MOD_SCREW", "MOD_VERTEX_WEIGHT", "MOD_DYNAMICPAINT", "MOD_REMESH", "MOD_OCEAN", "MOD_WARP", "MOD_SKIN", "MOD_TRIANGULATE", "MOD_WIREFRAME", "REC", "PLAY", "FF", "REW", "PAUSE", "PREV_KEYFRAME", "NEXT_KEYFRAME", "PLAY_AUDIO", "PLAY_REVERSE", "PREVIEW_RANGE", "ACTION_TWEAK", "PMARKER_ACT", "PMARKER_SEL", "PMARKER", "MARKER_HLT", "MARKER", "SPACE2", "SPACE3", "KEYINGSET", "KEY_DEHLT", "KEY_HLT", "MUTE_IPO_OFF", "MUTE_IPO_ON", "VISIBLE_IPO_OFF", "VISIBLE_IPO_ON", "DRIVER", "SOLO_OFF", "SOLO_ON", "FRAME_PREV", "FRAME_NEXT", "NLA_PUSHDOWN", "IPO_CONSTANT", "IPO_LINEAR", "IPO_BEZIER", "IPO_SINE", "IPO_QUAD", "IPO_CUBIC", "IPO_QUART", "IPO_QUINT", "IPO_EXPO", "IPO_CIRC", "IPO_BOUNCE", "IPO_ELASTIC", "IPO_BACK", "IPO_EASE_IN", "IPO_EASE_OUT", "IPO_EASE_IN_OUT", "VERTEXSEL", "EDGESEL", "FACESEL", "ROTATE", "CURSOR", "ROTATECOLLECTION", "ROTATECENTER", "ROTACTIVE", "ALIGN", "SMOOTHCURVE", "SPHERECURVE", "ROOTCURVE", "SHARPCURVE", "LINCURVE", "NOCURVE", "RNDCURVE", "PROP_OFF", "PROP_ON", "PROP_CON", "SCULPT_DYNTOPO", "PARTICLE_POINT", "PARTICLE_TIP", "PARTICLE_PATH", "MAN_TRANS", "MAN_ROT", "MAN_SCALE", "MANIPUL", "SNAP_OFF", "SNAP_ON", "SNAP_NORMAL", "SNAP_INCREMENT", "SNAP_VERTEX", "SNAP_EDGE", "SNAP_FACE", "SNAP_VOLUME", "STICKY_UVS_LOC", "STICKY_UVS_DISABLE", "STICKY_UVS_VERT", "CLIPUV_DEHLT", "CLIPUV_HLT", "SNAP_PEEL_OBJECT", "GRID", "PASTEDOWN", "COPYDOWN", "PASTEFLIPUP", "PASTEFLIPDOWN", "SNAP_SURFACE", "AUTOMERGE_ON", "AUTOMERGE_OFF", "RETOPO", "UV_VERTEXSEL", "UV_EDGESEL", "UV_FACESEL", "UV_ISLANDSEL", "UV_SYNC_SELECT", "BBOX", "WIRE", "SOLID", "SMOOTH", "POTATO", "ORTHO", "LOCKVIEW_OFF", "LOCKVIEW_ON", "AXIS_SIDE", "AXIS_FRONT", "AXIS_TOP", "NDOF_DOM", "NDOF_TURN", "NDOF_FLY", "NDOF_TRANS", "LAYER_USED", "LAYER_ACTIVE", "SORTALPHA", "SORTBYEXT", "SORTTIME", "SORTSIZE", "LONGDISPLAY", "SHORTDISPLAY", "GHOST", "IMGDISPLAY", "SAVE_AS", "SAVE_COPY", "BOOKMARKS", "FONTPREVIEW", "FILTER", "NEWFOLDER", "OPEN_RECENT", "FILE_PARENT", "FILE_REFRESH", "FILE_FOLDER", "FILE_BLANK", "FILE_BLEND", "FILE_IMAGE", "FILE_MOVIE", "FILE_SCRIPT", "FILE_SOUND", "FILE_FONT", "FILE_TEXT", "RECOVER_AUTO", "SAVE_PREFS", "LINK_BLEND", "APPEND_BLEND", "IMPORT", "EXPORT", "EXTERNAL_DATA", "LOAD_FACTORY", "LOOP_BACK", "LOOP_FORWARDS", "BACK", "FORWARD", "FILE_BACKUP", "DISK_DRIVE", "MATPLANE", "MATSPHERE", "MATCUBE", "MONKEY", "HAIR", "ALIASED", "ANTIALIASED", "MAT_SPHERE_SKY", "WORDWRAP_OFF", "WORDWRAP_ON", "SYNTAX_OFF", "SYNTAX_ON", "LINENUMBERS_OFF", "LINENUMBERS_ON", "SCRIPTPLUGINS", "SEQ_SEQUENCER", "SEQ_PREVIEW", "SEQ_LUMA_WAVEFORM", "SEQ_CHROMA_SCOPE", "SEQ_HISTOGRAM", "SEQ_SPLITVIEW", "IMAGE_RGB", "IMAGE_RGB_ALPHA", "IMAGE_ALPHA", "IMAGE_ZDEPTH", "IMAGEFILE", "BRUSH_ADD", "BRUSH_BLOB", "BRUSH_BLUR", "BRUSH_CLAY", "BRUSH_CLAY_STRIPS", "BRUSH_CLONE", "BRUSH_CREASE", "BRUSH_DARKEN", "BRUSH_FILL", "BRUSH_FLATTEN", "BRUSH_GRAB", "BRUSH_INFLATE", "BRUSH_LAYER", "BRUSH_LIGHTEN", "BRUSH_MASK", "BRUSH_MIX", "BRUSH_MULTIPLY", "BRUSH_NUDGE", "BRUSH_PINCH", "BRUSH_SCRAPE", "BRUSH_SCULPT_DRAW", "BRUSH_SMEAR", "BRUSH_SMOOTH", "BRUSH_SNAKE_HOOK", "BRUSH_SOFTEN", "BRUSH_SUBTRACT", "BRUSH_TEXDRAW", "BRUSH_THUMB", "BRUSH_ROTATE", "BRUSH_VERTEXDRAW", "MATCAP_01", "MATCAP_02", "MATCAP_03", "MATCAP_04", "MATCAP_05", "MATCAP_06", "MATCAP_07", "MATCAP_08", "MATCAP_09", "MATCAP_10", "MATCAP_11", "MATCAP_12", "MATCAP_13", "MATCAP_14", "MATCAP_15", "MATCAP_16", "MATCAP_17", "MATCAP_18", "MATCAP_19", "MATCAP_20", "MATCAP_21", "MATCAP_22", "MATCAP_23", "MATCAP_24", "VIEW3D_VEC", "EDIT_VEC", "EDITMODE_VEC_DEHLT", "EDITMODE_VEC_HLT", "DISCLOSURE_TRI_RIGHT_VEC", "DISCLOSURE_TRI_DOWN_VEC", "MOVE_UP_VEC", "MOVE_DOWN_VEC", "X_VEC", "SMALL_TRI_RIGHT_VEC"]
    BUILTIN_ICON_MESH_DATA = "MESH_DATA"
    BUILTIN_ICON_VOXELIZED = "GROUP_VERTEX" # GROUP_VERTEX, MESH_CUBE, MOD_REMESH
    BUILTIN_ICON_DOWN = "TRIA_DOWN"
    BUILTIN_ICON_RIGHT = "TRIA_RIGHT"

    ICON_VOXELIZED = "icon_voxelized"
    ICON_MESH_OBJECT = "icon_mesh_object"
    ICON_GREEN_CHECK = "icon_greencheck"
    ICON_EXCLAMATION = "icon_exclamation"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self.icons_dict = None
        self._initialized = True
        print("Initialized", self)

    def init(self) -> None:
        if self.icons_dict:
            return
        self.icons_dict = bpy.utils.previews.new()
        self.register_icons(IconsManager.ICON_EXCLAMATION, IconsManager.ICON_GREEN_CHECK)

    def register_icons(self, *icon_names):
        for icon_name in icon_names:
            self.register_icon(icon_name)

    def register_icon(self, icon_name):
        filename = icon_name + ".png" # svg supported in version 4.0+
        icon_path = os.path.join(FileUtils.get_addon_root_dir(), "resources", "icons", filename)
        return self.register_icon_path(icon_name, icon_path)

    def register_icon_path(self, icon_name, icon_path):
        # https://blender.stackexchange.com/questions/32335/how-to-implement-custom-icons-for-my-script-addon
        self.icons_dict.load(icon_name, icon_path, 'IMAGE')
        icon_value = self.icons_dict[icon_name].icon_id
        print(f"Registered icon {icon_value}: \"{icon_name}\"")
        return icon_value

    def get_icon_id(self, icon_name):
        icon_value = self.icons_dict[icon_name].icon_id
        return icon_value

    def cleanup(self) -> None:
        bpy.utils.previews.remove(self.icons_dict)
        self.icons_dict = None
        print("Icon cleanup complete")

# sample usage
# layout.label(text=item.name, icon=ICON_LIST[1])
# layout.label(text=item.name, icon_value=IconsManager().get_icon_id(IconsManager.ICON_NAME))