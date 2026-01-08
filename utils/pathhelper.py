import os
import sys

"""
Depricated.
Do not use
"""
def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for launch.exe.
    """
    if getattr(sys, 'frozen', False):
        # Running from launch.exe (PyInstaller/frozen)
        base_path = os.path.dirname(sys.executable)
    else:
        # Running from source (launch.py / main.py)
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Go one level up from utils/ to project root
        base_path = os.path.abspath(os.path.join(base_path, ".."))

    return os.path.abspath(os.path.join(base_path, relative_path))
