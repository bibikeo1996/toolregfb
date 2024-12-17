import os
import subprocess

def is_bluestacks_running():
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    return "HD-Player.exe" in result.stdout

def is_app_installed(adb_path, package_name):
    result = subprocess.run([adb_path, "shell", "pm", "list", "packages"], capture_output=True, text=True)
    return package_name in result.stdout