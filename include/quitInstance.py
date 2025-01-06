import subprocess
import os
import shutil
import time

from include.setUpDevices import ThietLapThongSoThietbi
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, ThoatInstance, ADBKillAndStartServer
from include.function import CapQuyenTruyCapChoFacebookLite, OpenApp, UnInstallAppFile
# from include.run import RunLD

def remove_all_pycache(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == "__pycache__":
                pycache_path = os.path.join(dirpath, dirname)
                shutil.rmtree(pycache_path)
                print(f"Đã xóa thư mục: {pycache_path}")


def Reboot(index, ld_path_console):
    command = f'{ld_path_console} reboot --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(10)
    return True

def LDOpened(index, ld_path_console):
    command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return True    

def OpenApp(index, ld_path_console, package_name):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to open app: {e}")
            return False
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")
        return False

def InstallAppFile(index, ld_path_console, apk_path):
    if ld_path_console:
        try:
            install_command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall app: {e}")        
            return False
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")
        return False

def UnInstallAppFile(index, ld_path_console, package_name):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall app: {e}")        
            return False
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")
        return False        

def RebootVaXoaCache(index, ld_path_console, package_name, apk_path):
    command = f'{ld_path_console} adb --index {index} --command "shell pm list packages"'
    # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell pm list packages"]
    result = subprocess.run(command, capture_output=True, text=True)
    # print(result.returncode)
    if result.returncode == 0:
        packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if ":" in line]
        for app in packages:
            if package_name.lower() in app.lower():
                UnInstallAppFile(index, ld_path_console, app)
                print("Deleting...")
    else:
        pass
    print("Rebooting...")                        
    isRebooted = Reboot(index, ld_path_console)
    while isRebooted:
        time.sleep(1)
        isOpenedLD = LDOpened(index, ld_path_console)
        if isOpenedLD:
            isInstalled = InstallAppFile(index, ld_path_console, apk_path)
            if isInstalled:
                return True
                break
        else:
            print("Đang chờ LDPlayer mở...")
    return False

# def RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance):
#     try:
#         if not all([ld_path_console, ld_path_instance]):
#             print("Đường dẫn ld_path_console hoặc ld_path_instance không hợp lệ.")
#             return False
#         # remove_all_pycache(".")
#         # Hàm kiểm tra LDPlayer có đang chạy không
#         def CheckLDPlayerRunning(index, ld_path_console):
#             command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
#             result = subprocess.run(command, shell=True, capture_output=True, text=True)
#             return "not found" not in result.stdout.lower() and "not found" not in result.stderr.lower()

#         # Kiểm tra LDPlayer có đang chạy hay không
#         CheckLDPlayerRunning = CheckLDPlayerRunning(index, ld_path_console)

#         if CheckLDPlayerRunning:
#             # TH1: Nếu LDPlayer đang chạy, thoát instance trước
#             # print(f"LDPlayer ld{index} đang chạy. Tiến hành thoát instance.")
#             if not ThoatInstance(index, ld_path_console):
#                 print(f"Không thể thoát instance ld{index}. Dừng tiến trình.")

#                 # ADBKillAndStartServer()

#                 # Xóa cache/logs
#                 instance_path = os.path.join(ld_path_instance, f"leidian{index}")
#                 logs_path = os.path.join(instance_path, "Logs")
#                 if os.path.exists(logs_path):
#                     shutil.rmtree(logs_path)
#                     print(f"Đã xóa thư mục Logs của instance ld{index} tại {logs_path}.")
#                 else:
#                     print(f"Không tìm thấy thư mục Logs tại {logs_path}.")

#                 # Thiết lập thông số thiết bị
#                 isSetup = ThietLapThongSoThietbi(index, ld_path_console)
#                 if isSetup:
#                     print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

#                 # Khởi động lại instance
#                 # print(f"Khởi động lại LDPlayer ld{index}.")
#                 isStarted = KhoiDongLDPlayer(index, ld_path_console)
#                 if(isStarted == True):
#                     pass

#                 # Bắt đầu các task sau khi instance đã khởi động thành công
#                 # print(f"Instance ld{index} đã khởi động thành công. Bắt đầu các tác vụ chung.")

#                 # Kiểm tra và cài đặt ứng dụng nếu cần
#                 isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
#                 if(isInstalled == True):
#                     pass

#                 # Cấp quyền và mở ứng dụng
#                 CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

#                 isOpened = OpenApp(index)
#                 while not isOpened:
#                     isOpened = OpenApp(index)

#         else:
#             # TH2: LDPlayer chưa chạy
#             print(f"LDPlayer ld{index} chưa chạy. Bắt đầu xử lý.")
#             pass

#             # Xóa cache/logs
#             instance_path = os.path.join(ld_path_instance, f"leidian{index}")
#             logs_path = os.path.join(instance_path, "Logs")
#             if os.path.exists(logs_path):
#                 shutil.rmtree(logs_path)
#                 print(f"Đã xóa thư mục Logs của instance ld{index} tại {logs_path}.")
#             else:
#                 print(f"Không tìm thấy thư mục Logs tại {logs_path}.")

#             # Thiết lập thông số thiết bị
#             isSetup = ThietLapThongSoThietbi(index, ld_path_console)
#             if isSetup:
#                 print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

#             # Khởi động lại instance
#             # print(f"Khởi động lại LDPlayer ld{index}.")
#             isStarted = KhoiDongLDPlayer(index, ld_path_console)
#             if(isStarted == True):
#                 pass

#             # Bắt đầu các task sau khi instance đã khởi động thành công
#             # print(f"Instance ld{index} đã khởi động thành công. Bắt đầu các tác vụ chung.")

#             # Kiểm tra và cài đặt ứng dụng nếu cần
#             isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
#             if(isInstalled == True):
#                 pass

#             # Cấp quyền và mở ứng dụng
#             CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

#             isOpened = OpenApp(index)
#             while not isOpened:
#                 isOpened = OpenApp(index)

#         return True

#     except Exception as e:
#         print(f"Lỗi trong quá trình thực thi: {e}")
#         return False

