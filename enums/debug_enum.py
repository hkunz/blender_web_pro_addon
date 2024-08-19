class DebugEnum():
    DEBUG_SKIP_INSTALL_CHECK = 1 # Skip installation check only for testing purposes. Should always be False in production
    DEBUG_WEB_TEST_OVERWRITE = 1 # Overwrite index.html, main.js, styles.css, on every web test button click
    DEBUG_USE_SYMLINK_COPY = 0 # Use symbolic links for index.html, main.js, styles.css instead of hard copies. Unfortuantely does not work with Three.js
    DEBUG_PROJECT_PATH = r"D:/KUNZ/Projects/blender/scripts/addons/blender_web_pro/test/test-project/"