import bpy

class InstallationPropertyGroup(bpy.types.PropertyGroup):
    INSTALLATION_STATUS_NOT_INSTALLED = 0
    INSTALLATION_STATUS_INSTALLED = 1
    INSTALLATION_STATUS_ERROR = 2

    DEBUG_SKIP_INSTALL_CHECK: bpy.props.BoolProperty(
        name="Check Installation",
        description="Skip installation check only for testing purposes. Should always be False in production",
        default=False,
    ) # type: ignore

    check_installation: bpy.props.BoolProperty(
        name="Check Installation",
        description="Check Installation for Chocolatey, Node.js, npm, npx, and nvm",
        default=True,
    ) # type: ignore

    installation_status_choco: bpy.props.IntProperty(
        name="Installation Status Chocolatey",
        description="Installation status of Chocolatey",
        default=INSTALLATION_STATUS_NOT_INSTALLED,
    ) # type: ignore

    installation_status_nodejs: bpy.props.IntProperty(
        name="Installation Status Node.js",
        description="Installation status of Node.js",
        default=INSTALLATION_STATUS_NOT_INSTALLED,
    ) # type: ignore

    installation_status_npm: bpy.props.IntProperty(
        name="Installation Status NPM",
        description="Installation status of NPM",
        default=INSTALLATION_STATUS_NOT_INSTALLED,
    ) # type: ignore

    installation_status_npx: bpy.props.IntProperty(
        name="Installation Status npx",
        description="Installation status of npx",
        default=INSTALLATION_STATUS_NOT_INSTALLED,
    ) # type: ignore

    installation_status_nvm: bpy.props.IntProperty(
        name="Installation Status NVM",
        description="Installation status of NVM",
        default=INSTALLATION_STATUS_NOT_INSTALLED,
    ) # type: ignore

    installed_choco_v: bpy.props.StringProperty(
        name="Installed Chocolatey version",
        default="",
    ) # type: ignore

    installed_nodejs_v: bpy.props.StringProperty(
        name="Installed Node.js version",
        default="",
    ) # type: ignore

    installed_npm_v: bpy.props.StringProperty(
        name="Installed NPM version",
        default="",
    ) # type: ignore

    installed_npx_v: bpy.props.StringProperty(
        name="Installed npx version",
        default="",
    ) # type: ignore

    installed_nvm_v: bpy.props.StringProperty(
        name="Installed NVM version",
        default="",
    ) # type: ignore