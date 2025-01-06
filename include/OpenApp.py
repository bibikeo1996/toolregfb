import os
import subprocess
import time
import sys
import psutil
from dotenv import load_dotenv
from tabulate import tabulate
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

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

def KhoiDongLDPlayer(index, ld_path_console):
    ldplayer_running = False
    while not ldplayer_running:
        command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
        # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell getprop"]
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
            start_command = [ld_path_console, "launch", "--index", str(index)]
            subprocess.run(start_command)
            # print(f"{result.stdout}")
            time.sleep(1)
        else:
            # print(f"LDPlayer {index} is already running")
            ldplayer_running = True
    return True       

def ThoatInstance(index, ld_path_console):
    """
    Hàm xử lý thoát một instance của LDPlayer.

    Args:
        index (int): Chỉ số của LDPlayer instance (vd: 0, 1, 2,...).
        ld_path_console (str): Đường dẫn đến công cụ LDPlayer console.

    Returns:
        bool: Trả về True nếu thoát thành công, False nếu có lỗi.
    """
    try:
        # Lệnh để thoát instance
        quit_command = f'{ld_path_console} quit --index {index}'
        result = subprocess.run(quit_command, capture_output=True, text=True)

        # Kiểm tra kết quả lệnh
        if result.returncode == 0:
            print(f"Đã thoát instance ld{index} thành công.")
            return True
        else:
            print(f"Lỗi khi thoát instance ld{index}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Lỗi trong quá trình thoát instance ld{index}: {e}")
        return False


def DemThoiGian(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rThời gian đợi: {remaining} giây")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")
    sys.stdout.flush()

# TrangThaiInstance(index, f"Instance {index} đã setup xong", saveText)
# def TrangThaiInstance(index, text, saveText={}):
#     saveText[index] = text
#     headers = [f"Index {i}" for i in saveText.keys()]
#     data = [[saveText[idx] for idx in saveText.keys()]]
#     table = tabulate(data, headers=headers, tablefmt="grid")
#     sys.stdout.write("\033[F" * (len(table.split("\n"))))
#     sys.stdout.write(table + "\n")
#     sys.stdout.flush()
            
def KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console):
    command = f'{ld_path_console} adb --index {index} --command "shell pm list packages"'
    # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell pm list packages"]
    result = subprocess.run(command, capture_output=True, text=True)
    # print(result.returncode)
    if result.returncode == 0:
        packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if ":" in line]
        for app in packages:
            if package_name.lower() in app.lower():
                return True
        install_command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
        # install_command = [ld_path_console, "adb", "--index", str(index), "--command", f"install {apk_path}"]
        install_result = subprocess.run(install_command, capture_output=True, text=True)
        print("Đang cài app Facebook Lite...")
        if install_result.returncode == 0:
            return True  # Sau khi cài thành công, trả về True
        else:
            print(f"Error installing {package_name}: {install_result.stderr}")
            return False  # Nếu cài không thành công, trả về False
    else:
        print(f"Error getting installed apps: {result.stderr}")
        return False  # Nếu không thể lấy danh sách ứng dụng, trả về False