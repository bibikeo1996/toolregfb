import os
import subprocess
import time
import sys
import psutil
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
# Đọc các biến môi trường
ld_path_console = os.getenv('LD_PATH_CONSOLE')  # Đường dẫn tới LDPlayer
ld_path_exe = os.getenv('LD_PATH_EXE')  # Đường dẫn tới LDPlayer
apk_path = os.getenv('APK_PATH')  # Đường dẫn tới file APK
package_name = os.getenv('PACKAGE_NAME')  # Tên gói của ứng dụng

def ADBKillAndStartServer():
    kill_command = ["adb", "kill-server"]
    subprocess.run(kill_command)
    # print("ADB server stopped")
    start_command = ["adb", "start-server"]
    subprocess.run(start_command)
    # print("ADB server started")

def KhoiDongLDPlayer(index):
    ldplayer_running = False
    while not ldplayer_running:
        command = ["ldconsole.exe", "adb", "--index", str(index), "--command", "shell getprop"]
        result = subprocess.run(command, capture_output=True, text=True)
        if "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
            start_command = ["ldconsole.exe", "launch", "--index", str(index)]
            subprocess.run(start_command)
            # print(f"{result.stdout}")
            time.sleep(1)
        else:
            # print(f"LDPlayer {index} is already running")
            ldplayer_running = True
    return True       

def TrangThaiInstance(index, text, saveText={}):
    saveText[index] = text
    headers = [f"Index {i}" for i in saveText.keys()]
    data = [[saveText[idx] for idx in saveText.keys()]]
    table = tabulate(data, headers=headers, tablefmt="grid")
    sys.stdout.write("\033[F" * (len(table.split("\n"))))
    sys.stdout.write(table + "\n")
    sys.stdout.flush()
            
def KiemTraDaCaiAppFaceBookLiteChua(index, target_app, apk_path):
    command = ["ldconsole.exe", "adb", "--index", str(index), "--command", "shell pm list packages"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.returncode)
    if result.returncode == 0:
        packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if ":" in line]
        for app in packages:
            if target_app.lower() in app.lower():
                return True
        install_command = [
            "ldconsole.exe", "adb", "--index", str(index), "--command", f"install {apk_path}"
        ]
        install_result = subprocess.run(install_command, capture_output=True, text=True)
        
        if install_result.returncode == 0:
            return True  # Sau khi cài thành công, trả về True
        else:
            print(f"Error installing {target_app}: {install_result.stderr}")
            return False  # Nếu cài không thành công, trả về False
    else:
        print(f"Error getting installed apps: {result.stderr}")
        return False  # Nếu không thể lấy danh sách ứng dụng, trả về False
