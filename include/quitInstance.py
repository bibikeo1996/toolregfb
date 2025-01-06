import subprocess
import os
import shutil
import time

from include.setUpDevices import ThietLapThongSoThietbi
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, ThoatInstance
from include.function import CapQuyenTruyCapChoFacebookLite, OpenApp, UnInstallAppFile
# from include.run import RunLD

def RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance):
    try:
        # Hàm kiểm tra LDPlayer có đang chạy không
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

        # Kiểm tra LDPlayer có đang chạy hay không
        ld_running = KhoiDongLDPlayer(index, ld_path_console)

        if ld_running:
            print(f"LDPlayer ld{index} đang chạy.")
            UnInstallAppFile(index, ld_path_console, package_name)
            ThoatInstance(index, ld_path_console)

        instance_path = os.path.join(ld_path_instance, f"leidian{index}")
        logs_path = os.path.join(instance_path, "Logs")
        if os.path.exists(logs_path):
            shutil.rmtree(logs_path)
            print(f"Đã xóa thư mục Logs của instance ld{index} tại {logs_path}.")
        else:
            print(f"Không tìm thấy thư mục Logs tại {logs_path}.")


        # Reboot LDPlayer
        isSetup = ThietLapThongSoThietbi(index, ld_path_console)
        if(isSetup == True):
            pass
        
        # Start LDPlayer
        isStarted = KhoiDongLDPlayer(index, ld_path_console)
        if isStarted:
            print(f"Đã khởi động LDPlayer ld{index}.")

        # Cài đặt ứng dụng nếu chưa có
        isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
        if not isInstalled:
            print("Tiến hành cài đặt ứng dụng.")
            # Thực hiện cài đặt (nếu cần)

        # Cấp quyền và mở ứng dụng
        CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

        OpenApp(index)

        return True

    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")
        return False
