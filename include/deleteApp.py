import subprocess
import os


def is_app_installed(package_name):
    """
    Kiểm tra xem app có được cài đặt không thông qua lệnh ADB.
    """
    result = os.popen(f"adb shell pm list packages | findstr {package_name}").read()
    return package_name in result


def xoa_app(adb_path, package_name):
    try:
        # Kiểm tra xem ứng dụng có được cài đặt không
        if not is_app_installed(package_name):
            print(f"Ứng dụng {package_name} không được cài đặt trên BlueStacks.")
            return

        # Xóa dữ liệu và cache trước khi gỡ cài đặt
        print(f"Đang xóa cache và dữ liệu ứng dụng {package_name}...")
        subprocess.run(
            [adb_path, "shell", "pm", "clear", package_name],
            capture_output=True,
            text=True,
        )
        print(f"Đã xóa cache và dữ liệu ứng dụng {package_name} thành công")

        # Thực hiện lệnh gỡ cài đặt
        print(f"Đang gỡ cài đặt ứng dụng {package_name}...")
        result = subprocess.run(
            [adb_path, "uninstall", package_name], capture_output=True, text=True
        )

        # Kiểm tra kết quả gỡ cài đặt
        if result.returncode == 0:
            print(f"Đã gỡ cài đặt thành công ứng dụng {package_name}.")
        else:
            print(f"Lỗi khi gỡ cài đặt ứng dụng {package_name}: {result.stderr}")
    except Exception as e:
        print(f"Không thể gỡ cài đặt ứng dụng {package_name}. Lỗi: {e}")
