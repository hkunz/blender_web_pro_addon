import bpy

class InstallationPropertyGroup(bpy.types.PropertyGroup):
    check_installation: bpy.props.BoolProperty(
        name="Check Installation",
        description="Check Installation for Chocolatey, Node.js, npm, npx, and nvm",
        default=True,
    ) # type: ignore