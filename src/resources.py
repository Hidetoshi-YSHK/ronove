import sys
import os.path as path
import enum

_RESOURCES_DIR = "resources"

class Resources(enum.Enum):
    OPEN_FILE_BUTTON = path.join(_RESOURCES_DIR, "open_file.png")
    PROCESS_BUTTON = path.join(_RESOURCES_DIR, "process.png")

    def get_path(self):
        TMP_DIR_ATTR = "_MEIPASS"
        if hasattr(sys, TMP_DIR_ATTR):
            tmp_dir = getattr(sys, TMP_DIR_ATTR)
            return path.join(tmp_dir, self.value)
        else:
            return path.join(self.value)
