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
        if not all([ld_path_console, ld_path_instance]):
            print("Đường dẫn ld_path_console hoặc ld_path_instance không hợp lệ.")
            return False

        # Hàm kiểm tra LDPlayer có đang chạy không
        def is_ldplayer_running(index, ld_path_console):
            command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return "not found" not in result.stdout.lower() and "not found" not in result.stderr.lower()

        # Kiểm tra LDPlayer có đang chạy hay không
        ld_running = is_ldplayer_running(index, ld_path_console)

        if ld_running:
            # TH1: Nếu LDPlayer đang chạy, thoát instance trước
            # print(f"LDPlayer ld{index} đang chạy. Tiến hành thoát instance.")
            if not ThoatInstance(index, ld_path_console):
                print(f"Không thể thoát instance ld{index}. Dừng tiến trình.")
                return False
        else:
            # TH2: LDPlayer chưa chạy
            print(f"LDPlayer ld{index} chưa chạy. Bắt đầu xử lý.")

        # Xóa cache/logs
        instance_path = os.path.join(ld_path_instance, f"leidian{index}")
        logs_path = os.path.join(instance_path, "Logs")
        if os.path.exists(logs_path):
            shutil.rmtree(logs_path)
            print(f"Đã xóa thư mục Logs của instance ld{index} tại {logs_path}.")
        else:
            print(f"Không tìm thấy thư mục Logs tại {logs_path}.")

        # Thiết lập thông số thiết bị
        isSetup = ThietLapThongSoThietbi(index, ld_path_console)
        if isSetup:
            print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

        # Khởi động lại instance
        # print(f"Khởi động lại LDPlayer ld{index}.")
        isStarted = KhoiDongLDPlayer(index, ld_path_console)
        if(isStarted == True):
            pass

        # Bắt đầu các task sau khi instance đã khởi động thành công
        # print(f"Instance ld{index} đã khởi động thành công. Bắt đầu các tác vụ chung.")

        # Kiểm tra và cài đặt ứng dụng nếu cần
        isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
        if(isInstalled == True):
            pass

        # Cấp quyền và mở ứng dụng
        CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

        OpenApp(index)

        print(f"Tất cả tác vụ đã hoàn tất cho LDPlayer ld{index}.")
        return True

    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")
        return False

