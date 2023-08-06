import os
import sys
import atexit
import hashlib


@atexit.register
def cleanup():
    try:
        if config.lock_file:
            config.lock_file.close()
        if config.fname:
            os.remove(config.fname)
    except Exception:
        pass


config = sys.modules[__name__]
config.file = None
config.fname = None
config.lock_file = None
config.maxinstances = 1


def configure_lock(
    maxinstances: int = 1,
    message: str | None = None,
    file: str | None = None,
) -> None:
    """
    Configures a lock file for a given file path and maximum number of instances.

    Args:
        maxinstances (int, optional): The maximum number of instances allowed to access the file. Defaults to 1.
        message (str, optional): The message to print if the maximum number of instances is reached. Defaults to None.
        file (str, optional): The file path to configure the lock file for. Defaults to None.


    Returns:
        None

    Raises:
        None
    """
    if not file:
        f = sys._getframe(1)
        dct = f.f_globals
        file = dct.get("__file__", "")
    config.file = os.path.normpath(file)
    config.maxinstances = int(maxinstances)

    for inst in range(config.maxinstances):
        try:
            hash = hashlib.sha256((config.file + f"{inst}").encode("utf-8", "ignore"))
            config.fname = hash.digest().hex() + ".locfi"
            tmpf = os.path.join(os.environ.get("TMP"), config.fname)
            if os.path.exists(tmpf):
                os.remove(tmpf)
            config.lock_file = os.open(tmpf, os.O_CREAT | os.O_EXCL)
            break
        except Exception as fe:
            if inst + 1 == config.maxinstances:
                if message:
                    print(message)
                try:
                    sys.exit(1)
                finally:
                    os._exit(1)
            else:
                continue
