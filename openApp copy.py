import os
import subprocess
import time

def open_bluestacks_and_search():
    # Đường dẫn tới tệp thực thi của BlueStacks (sửa lại nếu khác)
    bluestacks_path = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"
    adb_path = r"C:\Users\patroids115\Desktop\platform-tools-latest-windows\platform-tools\adb.exe"  # Đường dẫn đến adb.exe (nếu chưa có trong PATH)
    
    # Kiểm tra BlueStacks
    if not os.path.exists(bluestacks_path):
        print(f"Không tìm thấy BlueStacks tại: {bluestacks_path}")
        return

    try:
        # Mở BlueStacks
        subprocess.Popen([bluestacks_path])
        print("Đã mở BlueStacks thành công!")
        
        # Đợi BlueStacks khởi động (tăng thời gian nếu cần)
        time.sleep(30)  # Increase sleep time to ensure BlueStacks is fully started
        
        # Restart ADB server
        subprocess.run([adb_path, "kill-server"])
        subprocess.run([adb_path, "start-server"])
        time.sleep(5)  # Wait for ADB server to restart
        
        # Kiểm tra ADB
        adb_check = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        if "device" not in adb_check.stdout:
            print("Không tìm thấy thiết bị BlueStacks qua ADB. Hãy kiểm tra lại.")
            return
        
        # Gửi lệnh tìm kiếm trên CH Play
        search_command = f'{adb_path} shell am start -a android.intent.action.VIEW -d "market://search?q=Facebook Lite"'
        subprocess.run(search_command, shell=True)
        print("Đã tìm kiếm Facebook Lite trên cửa hàng!")

    except Exception as e:
        print(f"Không thể mở BlueStacks hoặc tìm kiếm Facebook Lite. Lỗi: {e}")

# Gọi hàm
open_bluestacks_and_search()
