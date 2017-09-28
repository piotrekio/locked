import platform
import subprocess


class ClipboardApplicationNotFound(OSError): pass


def set(value):
    if platform.system() == 'Linux':
        subprocess.run('xsel', input=value)
    else:
        raise ClipboardApplicationNotFound()


def clear():
    if platform.system() == 'Linux':
        subprocess.run(['xsel', '-c'])
    else:
        raise ClipboardApplicationNotFound()

