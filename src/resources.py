import sys
import os.path as path

def get_resource_path(relative_path):
    TMP_DIR_ATTR = "_MEIPASS"
    if hasattr(sys, TMP_DIR_ATTR):
        tmp_dir = getattr(sys, TMP_DIR_ATTR)
        return path.join(tmp_dir, relative_path)
    else:
        return path.join(relative_path)