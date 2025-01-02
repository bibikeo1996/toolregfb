import subprocess
import os
import shutil
import time

from include.setUpDevices import ThietLapThongSoThietbi
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer

def RebootVaXoaCache(index, ld_path_console, ld_path_instance):
    try:
        # Dừng LDPlayer instance trước khi xử lý
        stop_command = [ld_path_console, "quit", "--index", str(index)]
        subprocess.run(stop_command, check=True)
        print(f"Instance ld{index} đã được dừng.")
        time.sleep(2)

        # Đường dẫn thư mục của instance
        instance_path = os.path.join(ld_path_instance, f"leidian{index}")

        # Xóa thư mục Logs
        logs_path = os.path.join(instance_path, "Logs")
        if os.path.exists(logs_path):
            shutil.rmtree(logs_path)
            print(f"Đã xóa thư mục Logs của instance ld{index} tại {logs_path}.")
        else:
            print(f"Không tìm thấy thư mục Logs tại {logs_path}.")

        # Giữ nguyên các file vmdk, vbox, data
        print(f"Đã giữ nguyên các file cấu hình quan trọng trong {instance_path}.")

        # Thiết lập thông số thiết bị
        ThietLapThongSoThietbi(index, ld_path_console)
        time.sleep(1)

        return True

    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi xử lý reboot hoặc xóa cache: {e}")
        return False
    except Exception as e:
        print(f"Lỗi khác: {e}")
        return False

# def RebootVaXoaCache(index, ld_path_console, ld_path_instance):
#     try:
#         # Dừng LDPlayer instance trước khi xử lý
#         stop_command = [ld_path_console, "quit", "--index", str(index)]
#         subprocess.run(stop_command, check=True)
#         print(f"Instance ld{index} đã được dừng.")
#         time.sleep(2)
#         # Xóa toàn bộ thư mục config của instance
#         instance_path = os.path.join(ld_path_instance, f"leidian{index}")
#         if os.path.exists(instance_path):
#             shutil.rmtree(instance_path)
#             print(f"Đã xóa toàn bộ dữ liệu của instance ld{index} tại {instance_path}.")
#         else:
#             print(f"Không tìm thấy thư mục leidian{index} tại {instance_path}.")

#         ThietLapThongSoThietbi(index, ld_path_console)
#         time.sleep(1)

#         return True

#     except subprocess.CalledProcessError as e:
#         print(f"Lỗi khi xử lý reboot hoặc xóa cache: {e}")
#         return False
#     except Exception as e:
#         print(f"Lỗi khác: {e}")
#         return False


# ld_path_console = "D:\\LDPlayer\\LDPlayer9\\ldconsole.exe"
# ld_path_instance = "D:\\LDPlayer\\LDPlayer9\\vms\\"
# index = 1

# if RebootVaXoaCache(index, ld_path_console, ld_path_instance):
#     print("Reboot và xóa cache thành công!")
# else:
#     print("Có lỗi xảy ra khi reboot và xóa cache.")