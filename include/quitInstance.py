import subprocess
import os
import shutil
import time
import pyautogui

from include.setUpDevices import *
from include.OpenApp import *
from include.function import *
# from include.run import RunLD

def ADBKillAndStartServer():
    kill_command = ["adb", "kill-server"]
    subprocess.run(kill_command)
    time.sleep(2)
    # print("ADB server stopped")
    start_command = ["adb", "start-server"]
    subprocess.run(start_command)
    time.sleep(2)
    # start_command = ["adb", "devices"]
    # subprocess.run(start_command)
    # time.sleep(5)

## Khởi dộng LDPlayer
def StartLD(index, ld_path_console):
    command = f'{ld_path_console} launch --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    DemThoiGian(13)
    return False

def ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port):
    try:   
        encoded_password = urllib.parse.quote(proxy_password)
        command = f'{ld_path_console} adb --index {index} --command "shell settings put global http_proxy {proxy_username}:{encoded_password}@{proxy_ip}:{proxy_port}"'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
            print("Ko thể connect Proxy:", result.stderr)
    except FileNotFoundError:
        print(f"Không tìm thấy ldconsole.exe tại: {ldconsole_path}")
    DemThoiGian(2)        

def RemoveProxy(index, ld_path_console, proxy_ip, proxy_port):
    try:
        command = f'{ld_path_console} adb --index {index} --command "shell settings delete global http_proxy"'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
            print("Ko thể remove Proxy:", result.stderr)
    except FileNotFoundError:
        print(f"Không tìm thấy ldconsole.exe tại: {ldconsole_path}")        

def ClearCache(index, ld_path_instance):
    try:
        # Xác định đường dẫn thư mục cache cần xóa
        cache_folder = os.path.join(ld_path_instance, f'leidian{index}')
        if os.path.exists(cache_folder):
            # Xóa thư mục và toàn bộ nội dung bên trong
            shutil.rmtree(cache_folder)
            print(f"Đã xóa thành công thư mục cache: {cache_folder}")
            return True
        else:
            print(f"Không tìm thấy thư mục cache tại: {cache_folder}")
            return False
    except Exception as e:
        print(f"Lỗi khi xóa thư mục cache: {e}")
        return False

## Check facebook có tồn tại hay không sau đó uninstall
def UninstallFacebook(index, ld_path_console, package_name, timeout=20):
    subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(2)
    return True

## Cài facebook
def InstallFacebook(template_path, index, ld_path_console, apk_path, timeout=20):
    command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # print("Installing Facebook...")
    DemThoiGian(5)
    return True

## Mở app Facebook
def OpenApp(template_path, index, ld_path_console, package_name, timeout=20):
    subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
    start_time = time.time()
    DemThoiGian(5)
    return True

def KillApp(index, ld_path_console, package_name):
    subprocess.run([ld_path_console, 'killapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(2)
    return True

def QuitLD(index, ld_path_console):
    command = f'{ld_path_console} quit --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    DemThoiGian(2)
    return True