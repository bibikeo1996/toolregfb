import os
import subprocess
import time

def isBlueStackRunning(bluestacks_path, adb_path, apk_path, package_name):
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    if "HD-Player.exe" in result.stdout:
        print("BlueStacks đã được mở.")
    else:
        print("Đang mở BlueStacks...")
        subprocess.Popen([bluestacks_path])
        time.sleep(12)  # Đợi BlueStacks khởi động (tăng thời gian nếu cần)

    # Restart ADB server
    print("Đang khởi động lại ADB server...")
    subprocess.run([adb_path, "kill-server"])
    subprocess.run([adb_path, "start-server"])

    # Check ADB connection
    adb_check = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
    if "device" not in adb_check.stdout:
        print("Không tìm thấy thiết bị BlueStacks qua ADB. Hãy kiểm tra lại.")
        return False

    # Check if APK exists
    if not os.path.exists(apk_path):
        print(f"Không tìm thấy tệp APK tại: {apk_path}")
        return False

    # Check if BlueStacks exists
    if not os.path.exists(bluestacks_path):
        print(f"Không tìm thấy BlueStacks tại: {bluestacks_path}")
        return False

    # Install APK if not installed
    if not is_app_installed(adb_path, package_name):
        print(f"Đang cài đặt APK từ {apk_path} vào BlueStacks...")
        install_command = [adb_path, "install", apk_path]
        result = subprocess.run(install_command, capture_output=True, text=True)
        
        # Check installation result
        if result.returncode == 0:
            print("Cài đặt APK thành công!")
        else:
            print(f"Lỗi khi cài đặt APK: {result.stderr}")
            return False
    else:
        print("Ứng dụng Facebook Lite đã được cài đặt.")

    return True

def is_app_installed(adb_path, package_name):
    result = subprocess.run([adb_path, "shell", "pm", "list", "packages"], capture_output=True, text=True)
    return package_name in result.stdout

def isAPKexist(apk_path):
    if not os.path.exists(apk_path):
        print(f"Không tìm thấy tệp APK tại: {apk_path}")
        return

def isBlueStacksexist(bluestacks_path):
    if not os.path.exists(bluestacks_path):
        print(f"Không tìm thấy BlueStacks tại: {bluestacks_path}")
        return