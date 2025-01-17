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
    time.sleep(1)
    # print("ADB server stopped")
    start_command = ["adb", "start-server"]
    subprocess.run(start_command)
    time.sleep(2)

## Khởi dộng LDPlayer
def StartLD(template_path, index, ld_path_console):
    command = f'{ld_path_console} launch --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    for _ in range(30):  # Lặp tối đa 30 lần (tương đương với 1 phút nếu sleep 2 giây)
        try:
            pos = TimAnhSauKhiChupVaSoSanhv2(template_path, index, ld_path_console)
            if pos is not None:
                print("Start LDPlayer successfully")
                return True  # Thoát khỏi hàm khi tìm thấy
            else:
                time.sleep(2)
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(2)

    print("Không tìm thấy pos trong thời gian giới hạn.")
    return False  # Trả về `False` nếu hết thời gian

def ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port):
    try: 
        # ADBKillAndStartServer()
        start_command = ["adb", "devices"]
        subprocess.run(start_command)
        DemThoiGian(2)
        """
        Cấu hình proxy cho emulator dựa trên index.
        
        :param index: Index của emulator (bắt đầu từ 0).
        :param proxy_ip: Địa chỉ IP của proxy.
        :param proxy_port: Cổng của proxy.
        """
        # Tính port dựa trên index
        port = 5555 + index * 2
        removeproxy = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy :0'
        result = subprocess.run(removeproxy, capture_output=True, text=True)
        # Lệnh ADB để cấu hình proxy
        DemThoiGian(1)
        command = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy {proxy_ip}:{proxy_port}'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
            print(f"Proxy set thành công trên {index} (port {port})")
        else:
            return False
            print(f"Lỗi khi set proxy trên emulator {index} (port {port}): {result.stderr}")
    except FileNotFoundError:
        print(f"Không tìm thấy ldconsole.exe tại: {ldconsole_path}")
    DemThoiGian(2)
    # checkProxy = f'{ld_path_console} adb --index {index} --command "shell settings get global http_proxy"' 

def RemoveProxy(index, ld_path_console):
    try:
        port = 5555 + index * 2
        command = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy :0'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
            print(f"Tắt proxy thành công trên {index} (port {port})")
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
def OpenApp(index, ld_path_console, package_name):
    subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(4)
    return True

def KillApp(index, ld_path_console, package_name):
    subprocess.run([ld_path_console, 'killapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(2)
    return True

def QuitLD(index, ld_path_console, ld_path_instance):
    RemoveProxy(index, ld_path_console)
    DemThoiGian(2)
    command = f'{ld_path_console} quit --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    DemThoiGian(1)
    # ClearCache(index, ld_path_instance)
    return True

## Mở app Proxifier
def OpenProxifer(index, ld_path_console, package_name):
    subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(4)
    return True    