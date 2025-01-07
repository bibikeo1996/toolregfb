import subprocess
import os
import shutil
import time
import pyautogui

from include.setUpDevices import ThietLapThongSoThietbi
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, ThoatInstance, ADBKillAndStartServer, DemThoiGian
from include.function import CapQuyenTruyCapChoFacebookLite
# from include.run import RunLD

# def remove_all_pycache(root_dir):
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         for dirname in dirnames:
#             if dirname == "__pycache__":
#                 pycache_path = os.path.join(dirpath, dirname)
#                 shutil.rmtree(pycache_path)
#                 print(f"Đã xóa thư mục: {pycache_path}")

# def Reboot(index, ld_path_console):
    # command = f'{ld_path_console} reboot --index {index}'
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # DemThoiGian(10)
    # return True

# def CheckLDPlayerRunning(index, ld_path_console):
#     command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     return "not found" not in result.stdout.lower() and "not found" not in result.stderr.lower()

# def OpenLD(index, ld_path_console):
#     ldplayer_running = False
#     command = f'{ld_path_console} launch --index {index}'
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     DemThoiGian(15)
#     # while not ldplayer_running:
#     #     command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
#     #     # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell getprop"]
#     #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     #     if "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
#     #         start_command = [ld_path_console, "launch", "--index", str(index)]
#     #         subprocess.run(start_command)
#     #         # print(f"{result.stdout}")
#     #         time.sleep(1)
#     #     else:
#     #         # print(f"LDPlayer {index} is already running")
#     #         ldplayer_running = True
#     return True 

# def LDOpened(template_path, index, ld_path_console):
#     command = f'{ld_path_console} launch --index {index}'
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     while True:
#         try:
#             location = pyautogui.locateOnScreen(template_path, confidence=0.9)
#             if location:
#                 return location
#         except pyautogui.ImageNotFoundException:
#             pass
#         time.sleep(0.5)
    
#     # start_time = time.time()
#     # while time.time() - start_time < timeout:
#     #     location = pyautogui.locateOnScreen(template_path, confidence=0.9)
#     #     if location:
#     #         return True
#     #     time.sleep(0.5)
#     # return False

# def InstallAppFile(index, ld_path_console, apk_path):
#     if ld_path_console:
#         try:
#             install_command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
#             result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"Failed to uninstall app: {e}")        
#             return False
#     else:
#         print("LD_PATH_CONSOLE environment variable is not set.")
#         return False

# def UnInstallAppFile(index, ld_path_console, package_name):
#     if ld_path_console:
#         try:
#             subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"Failed to uninstall app: {e}")        
#             return False
#     else:
#         print("LD_PATH_CONSOLE environment variable is not set.")
#         return False        

# def RebootVaXoaCache(index, ld_path_console, package_name, apk_path):
#     command = f'{ld_path_console} adb --index {index} --command "shell pm list packages"'
#     # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell pm list packages"]
#     result = subprocess.run(command, capture_output=True, text=True)
#     # print(result.returncode)
#     if result.returncode == 0:
#         packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if ":" in line]
#         for app in packages:
#             if package_name.lower() in app.lower():
#                 UnInstallAppFile(index, ld_path_console, app)
#                 print("Deleting...")
#     else:
#         pass
#     if CheckLDPlayerRunning(index, ld_path_console):
#         print("Rebooting...")                        
#         isRebooted = Reboot(index, ld_path_console)
#         while isRebooted:
#             time.sleep(1)
#             isOpenedLD = LDOpened(index, ld_path_console)
#             if isOpenedLD:
#                 isInstalled = InstallAppFile(index, ld_path_console, apk_path)
#                 if isInstalled:
#                     return True
#                     break
#             else:
#                 print("Đang chờ LDPlayer mở...")
#     else:  
#         print("Opening LDPlayer...")
#         isOpened = OpenLD(index, ld_path_console)
#         while isOpened:
#             time.sleep(1)
#             isOpenedLD = LDOpened(index, ld_path_console)
#             if isOpenedLD:
#                 isInstalled = InstallAppFile(index, ld_path_console, apk_path)
#                 if isInstalled:
#                     return True
#                     break
#             else:
#                 print("Đang chờ LDPlayer mở...")
#     return False

## Mở app Facebook
def OpenApp(template_path, index, ld_path_console, package_name, timeout=10):
    subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            return False
        time.sleep(0.5)
    return False

## Check LDPlayer đang chạy hay không
def isLDRunning(template_path, index, timeout=10):
    while True:
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            return False
        time.sleep(0.5)
    return False

## Khởi dộng LDPlayer
def StartLD(template_path, index, ld_path_console):
    command = f'{ld_path_console} launch --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    while True:
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    return False 

## Check facebook có tồn tại hay không sau đó uninstall
def isFacebookExist(template_path, index, ld_path_console, package_name, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
                return True
        except pyautogui.ImageNotFoundException:
            pass                
        time.sleep(0.5)
    return False

## Cài facebook
def isFacebookInstall(template_path, index, ld_path_console, apk_path, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    return False  

## Reboot và xóa cache
def isRebooting(template_path, index, ld_path_console, timeout=10):
    command = f'{ld_path_console} reboot --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=0.9)
            if location:
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    return False     

