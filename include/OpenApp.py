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

def KhoiDongLDPlayer(index):
    ldplayer_running = False
    while not ldplayer_running:
        command = ["ldconsole.exe", "adb", "--index", str(index), "--command", "shell getprop"]
        result = subprocess.run(command, capture_output=True, text=True)
        if "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
            start_command = ["ldconsole.exe", "launch", "--index", str(index)]
            subprocess.run(start_command)
            time.sleep(1)
        else:
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


# def is_ldplayer_running():
#     """Kiểm tra xem LDPlayer.exe có đang chạy hay không."""
#     for proc in psutil.process_iter(['pid', 'name']):
#         print(f"{proc.info['name'].lower()}")
#         if proc.info['name'].lower() == 'ldplayer.exe':
#             return True
#     return False

# def start_ldplayer():
#     try:
#         # Kiểm tra xem LDPlayer.exe có tồn tại hay không
#         if not os.path.exists(ld_path_exe):
#             raise FileNotFoundError(f"Không tìm thấy LDPlayer.exe tại {ld_path_exe}")
        
#         # Khởi động LDPlayer.exe
#         start_command = f'"{ld_path_exe}"'  # Chạy LDPlayer.exe
#         subprocess.Popen(start_command, shell=True)  # Sử dụng Popen để không đợi đến khi LDPlayer hoàn tất
        
#         print("LDPlayer đang khởi động...")
#     except Exception as e:
#         print(f"Failed to start LD Player: {e}")

# def install_apk():
#     try:
#         # Kiểm tra xem ldconsole.exe và APK có tồn tại không
#         if not os.path.exists(ld_path_console):
#             raise FileNotFoundError(f"Không tìm thấy ldconsole.exe tại {ld_path_console}")
#         if not os.path.exists(apk_path):
#             raise FileNotFoundError(f"Không tìm thấy file APK tại {apk_path}")
        
#         # Lệnh cài đặt ứng dụng thông qua ldconsole.exe
#         install_command = f'"{ld_path_console}" installapp "{apk_path}"'
        
#         # Thực thi lệnh cài đặt
#         subprocess.run(install_command, shell=True, check=True)
        
#         print("Cài đặt ứng dụng thành công.")
    
#     except Exception as e:
#         print(f"Lỗi khi cài đặt ứng dụng: {e}")


# if ld_path_console and apk_path and package_name:
#     try:
#        install_apk()

#     except subprocess.CalledProcessError as e:
#         print(f"Failed to open LD Player, install APK, or launch app: {e}")
# else:
#     print("LD_PATH_CONSOLE, APK_PATH, or PACKAGE_NAME not found in .env file")