import os
import subprocess
import time

def is_bluestacks_running():
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    return "HD-Player.exe" in result.stdout

def is_app_installed(adb_path, package_name):
    result = subprocess.run([adb_path, "shell", "pm", "list", "packages"], capture_output=True, text=True)
    return package_name in result.stdout

def open_bluestacks_and_install_apk(apk_path):
    bluestacks_path = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"  # Đường dẫn tới BlueStacks (cập nhật nếu cần)
    adb_path = r"C:\Users\patroids115\Desktop\platform-tools-latest-windows\platform-tools\adb.exe"  # Đường dẫn tới adb.exe
    package_name = "com.facebook.lite"

    # Kiểm tra tệp APK
    if not os.path.exists(apk_path):
        print(f"Không tìm thấy tệp APK tại: {apk_path}")
        return
    
    # Kiểm tra BlueStacks
    if not os.path.exists(bluestacks_path):
        print(f"Không tìm thấy BlueStacks tại: {bluestacks_path}")
        return

    try:
        # Mở BlueStacks nếu chưa mở
        if not is_bluestacks_running():
            print("Đang mở BlueStacks...")
            subprocess.Popen([bluestacks_path])
            time.sleep(30)  # Đợi BlueStacks khởi động (tăng thời gian nếu cần)
        else:
            print("BlueStacks đã được mở.")

        # Restart ADB server để đảm bảo kết nối với BlueStacks
        print("Đang khởi động lại ADB server...")
        subprocess.run([adb_path, "kill-server"])
        subprocess.run([adb_path, "start-server"])
        time.sleep(5)  # Đợi ADB server khởi động lại
        
        # Kiểm tra kết nối ADB
        adb_check = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        if "device" not in adb_check.stdout:
            print("Không tìm thấy thiết bị BlueStacks qua ADB. Hãy kiểm tra lại.")
            return
        
        # Cài đặt APK nếu chưa cài
        if not is_app_installed(adb_path, package_name):
            print(f"Đang cài đặt APK từ {apk_path} vào BlueStacks...")
            install_command = [adb_path, "install", apk_path]
            result = subprocess.run(install_command, capture_output=True, text=True)
            
            # Kiểm tra kết quả cài đặt
            if result.returncode == 0:
                print("Cài đặt APK thành công!")
            else:
                print(f"Lỗi khi cài đặt APK: {result.stderr}")
                return
        else:
            print("Ứng dụng Facebook Lite đã được cài đặt.")
        
        # Mở ứng dụng Facebook Lite
        print("Đang mở ứng dụng Facebook Lite...")
        start_app_command = [adb_path, "shell", "am", "start", "-n", "com.facebook.lite/.MainActivity"]
        subprocess.run(start_app_command)
        time.sleep(5)  # Đợi ứng dụng khởi động

        coordinates = {
            1: (150, 1285),
            2: (450, 1285),
            3: (750, 1285),
            4: (150, 1375),
            5: (450, 1375),
            6: (750, 1375),
            7: (150, 1465),
            8: (450, 1465),
            9: (750, 1465),
            0: (450, 1555)
        }
        date_string = "15/10/1996"

        # Nhập dữ liệu test
        print("Đang nhập dữ liệu test...")
        #tạo tài khoản
        subprocess.run([adb_path, "shell", "input", "tap", "450", "551"])
        
        #Click tiếp
        subprocess.run([adb_path, "shell", "input", "tap", "450", "551"])
        
        # nhập tên và họ 
        subprocess.run([adb_path, "shell", "input", "tap", "232", "319"])
        subprocess.run([adb_path, "shell", "input", "text", "John"])

        time.sleep(1)
        subprocess.run([adb_path, "shell", "input", "tap", "667", "319"])
        subprocess.run([adb_path, "shell", "input", "text", "Pham"])

        time.sleep(1)
        #  click tiếp 
        subprocess.run([adb_path, "shell", "input", "tap", "450", "388"])
        # Chọn email 
        subprocess.run([adb_path, "shell", "input", "tap", "450", "475"])
        subprocess.run([adb_path, "shell", "input", "text", "testemaillau@gmail.com"])

        #click tiếp sau khi nhập email
        subprocess.run([adb_path, "shell", "input", "tap", "450", "376"])

        # Nhập ngày sinh theo định dạng dd/mm/yyyy
        tap_commands = []
        for char in date_string:
            if char.isdigit():  # Kiểm tra nếu ký tự là số
                num = int(char)
                if num in coordinates:  # Kiểm tra tọa độ hợp lệ
                    x, y = coordinates[num]
                    tap_commands.append([adb_path, "shell", "input", "tap", str(x), str(y)])

        for command in tap_commands:
            subprocess.run(command)
            #print(f"Tapped at {command[4]}, {command[5]}")
        #click tiếp sau khi chọn ngày sinh 
        subprocess.run([adb_path, "shell", "input", "tap", "450", "416"]) 

        #chọn giới tính 
        subprocess.run([adb_path, "shell", "input", "tap", "450", "382"]) 

        subprocess.run([adb_path, "shell", "input", "tap", "449", "327"])
        subprocess.run([adb_path, "shell", "input", "text", "John@123"])
        time.sleep(1)

        #click tiếp sau khi nhập mật khẩu
        subprocess.run([adb_path, "shell", "input", "tap", "450", "396"])

        #click đăng ký
        subprocess.run([adb_path, "shell", "input", "tap", "450", "431"])
        print("Đã hoàn thành việc nhập dữ liệu test!")

    except Exception as e:
        print(f"Không thể cài đặt APK hoặc nhập dữ liệu test. Lỗi: {e}")

# Gọi hàm với đường dẫn tới APK
apk_path = r"D:\Workspace\python-app\fblite.apk"  # Đổi đường dẫn tới APK bạn muốn cài
open_bluestacks_and_install_apk(apk_path)