import os
import subprocess
import time
import requests
from dotenv import load_dotenv
from include.detectButton import click_button_by_text, wait_for_element
from include.isAppRunning import is_bluestacks_running, is_app_installed
from include.detectFields import detect_field_type, input_text_into_fields
import include.defined as defined
# Load biến môi trường từ tệp .env nếu có
load_dotenv()

bluestacks_path = os.getenv('BLUESTACKS_PATH')
adb_path = os.getenv('ADB_PATH')
package_name = os.getenv('PACKAGE_NAME')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')

def open_bluestacks_and_install_apk(apk_path):
    # Cấu hình proxy cho ScraperAPI
    proxy = f"http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001"
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
            time.sleep(12)  # Đợi BlueStacks khởi động (tăng thời gian nếu cần)
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

         
        print("Đang kiểm tra kết nối proxy từ ứng dụng di động...")
        check_proxy_command = [adb_path, "shell", "curl", "http://httpbin.org/ip"]
        result = subprocess.run(check_proxy_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"IP trả về từ proxy: {result.stdout}")
        else:
            print(f"Lỗi khi kiểm tra proxy: {result.stderr}")   

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

        # Nhập dữ liệu test
        print("Đang nhập dữ liệu test...")

        if wait_for_element(adb_path, defined.noneOfTheABove):
            pass
        else: 
            pass
        time.sleep(1)

        #tạo tài khoản
        if wait_for_element(adb_path, defined.createBtn):
            pass
        time.sleep(1)
        if wait_for_element(adb_path, defined.getStartedBtn):
            pass
        else:
            pass
        time.sleep(1)
        textFullName = ["John", "Doe"]
        field_coordinates = detect_field_type(adb_path, "EditText")
        if input_text_into_fields(adb_path, field_coordinates, textFullName):
            pass
        else:
            print("Không thể nhập tất cả các trường.")
            return
        time.sleep(1)

        # if wait_for_element(adb_path, defined.setBtn):
        #     pass
        # tiếp
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "737"])
        # time.sleep(1)

        # # Nhập họ tên
        # subprocess.run([adb_path, "shell", "input", "tap", "205", "294"])
        # subprocess.run([adb_path, "shell", "input", "text", "Pham"])
        # time.sleep(1)

        # subprocess.run([adb_path, "shell", "input", "tap", "640", "294"])
        # subprocess.run([adb_path, "shell", "input", "text", "John"])
        # time.sleep(1)

        # subprocess.run([adb_path, "shell", "input", "tap", "450", "389"])

        # # chọn ngày tháng năm sinh
        # subprocess.run([adb_path, "shell", "input", "swipe", "116", "826", "116", "926", "300"])
        # time.sleep(1)
        # subprocess.run([adb_path, "shell", "input", "swipe", "236", "826", "236", "926", "300"])
        # time.sleep(1)
        # subprocess.run([adb_path, "shell", "input", "swipe", "356", "826", "356", "2826", "300"])
        # time.sleep(1)

        # #click đặt
        # subprocess.run([adb_path, "shell", "input", "tap", "656", "1078"])
        # time.sleep(1)

        # # click tiếp
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "418"])
        # time.sleep(1)

        # # chọn giới tính 
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "309"])
        # #subprocess.run([adb_path, "shell", "input", "tap", "450", "393"])
        # time.sleep(1)

        # # click tiếp
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "579"])
        # time.sleep(1)


        # for i in range(3, 0, -1):
        #     print(f"Đếm lùi: {i} giây")
        #     time.sleep(1)  # Dừng lại 1 giây mỗi lần

        # print("Deny access dialog")
        # subprocess.run([adb_path, "shell", "input", "tap", "574", "857"])
        # time.sleep(1)
        # # click deny to access dialog

        # # chọn email
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "552"])
        # time.sleep(1)
        
        # subprocess.run([adb_path, "shell", "input", "text", "kz46zbc7umb@gmail.com"])
        # time.sleep(1)

        # # click tiếp
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "439"])
        # time.sleep(1)

        # #click nhập mật khẩu
        # subprocess.run([adb_path, "shell", "input", "tap", "423", "323"])
        # subprocess.run([adb_path, "shell", "input", "text", "matkhau@1123"])
        # time.sleep(1)

        # subprocess.run([adb_path, "shell", "input", "tap", "450", "418"])
        # time.sleep(1)

        # subprocess.run([adb_path, "shell", "input", "tap", "450", "297"])
        # time.sleep(1)

        # # đồng ý điều khoản
        # subprocess.run([adb_path, "shell", "input", "tap", "450", "1471"])
        # time.sleep(1)

        print("Đã hoàn thành việc nhập dữ liệu test!")

    except Exception as e:
        print(f"Không thể cài đặt APK hoặc nhập dữ liệu test. Lỗi: {e}")

# Gọi hàm với đường dẫn tới APK
apk_path = os.getenv('APK_PATH')  # Đổi đường dẫn tới APK bạn muốn cài
open_bluestacks_and_install_apk(apk_path)