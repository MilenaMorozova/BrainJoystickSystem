import os
import tempfile

from settings import TEMP_FILES_PREFIX


def delete_all_temp_files():
    temp_dir = tempfile._get_default_tempdir()
    files = filter(lambda f: f.startswith(TEMP_FILES_PREFIX), os.listdir(temp_dir))

    for file in files:
        os.remove(os.path.join(temp_dir, file))
