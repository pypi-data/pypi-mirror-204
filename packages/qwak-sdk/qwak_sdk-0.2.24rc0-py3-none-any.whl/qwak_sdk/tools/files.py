import shutil
import sys


def copytree(*args, **kwargs):
    if sys.version_info.minor == 7:
        kwargs.pop("dirs_exist_ok", None)

    shutil.copytree(*args, **kwargs)
