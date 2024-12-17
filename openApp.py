import os
import subprocess
import time
import random
import requests
from dotenv import load_dotenv
from include.detectButton import ClickVaoButtonTrungText, DoiElementLoad, ClickVaoClassName
from include.isAppRunning import is_bluestacks_running, is_app_installed
from include.detectFields import XacDinhLoaiField, NhapTextVaoField
from include.detectNumPicker import ChonNgayThangNamSinh
from validate.validate import KiemTraElementCoTonTaiKhong, KiemTraClassCoTonTai
from validate.proxy import KiemTraProxy
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

        # if KiemTraProxy(adb_path):
        #     pass
        # else:
        #     return False 

        # Mở ứng dụng Facebook Lite
        print("Đang mở ứng dụng Facebook Lite...")
        start_app_command = [adb_path, "shell", "am", "start", "-n", "com.facebook.lite/.MainActivity"]
        subprocess.run(start_app_command)
        #time.sleep(5)  # Đợi ứng dụng khởi động

        # Nhập dữ liệu test
        print("Đang nhập dữ liệu test...")

        if DoiElementLoad(adb_path, defined.noneOfTheABove):
            pass
        else: 
            pass

        #tạo tài khoản
        if DoiElementLoad(adb_path, defined.createBtn):
            pass

        if DoiElementLoad(adb_path, defined.getStartedBtn):
            pass
        else:
            pass

        textFullName = ["John", "Doe"]
        ToaDoField = XacDinhLoaiField(adb_path, "EditText")
        if NhapTextVaoField(adb_path, ToaDoField, textFullName):
            pass
        else:
            print("Không thể nhập tất cả các trường.")
            return

        if DoiElementLoad(adb_path, defined.nextBtn):
            pass

        if KiemTraClassCoTonTai(adb_path, defined.useadifferentnameBtn):
            ClickVaoClassName(adb_path, "android.widget.RadioButton")
            DoiElementLoad(adb_path, defined.nextBtn)
            pass
        else: 
            pass

        if (KiemTraElementCoTonTaiKhong(adb_path, element_id="android:id/numberpicker_input")):
            time.sleep(1)
            interactive_elements = ChonNgayThangNamSinh(adb_path, specific_id="android:id/numberpicker_input")
        else:
            print("Không thể tìm thấy element.")
            return

        if DoiElementLoad(adb_path, defined.setBtn):
            pass

        if DoiElementLoad(adb_path, defined.nextBtn):
            pass    

        ## Chọn giới tính
        if DoiElementLoad(adb_path, defined.isMale):
            gender = random.choice([defined.isMale, defined.isFemale])
            ClickVaoButtonTrungText(adb_path, gender)
            pass    

        if DoiElementLoad(adb_path, defined.nextBtn):
            pass

        ## Kiểm tra cho phép Facebook truy cập danh bạ
        if KiemTraElementCoTonTaiKhong(adb_path, element_id="'com.android.packageinstaller:id/permission_deny_button"):
            ClickVaoButtonTrungText(adb_path, defined.denyBtn)
            pass

        ## Kiểm tra cho phép Facebook gọi điện
        if KiemTraElementCoTonTaiKhong(adb_path, element_id="'com.android.packageinstaller:id/permission_deny_button"):
            ClickVaoButtonTrungText(adb_path, defined.denyBtn)
            pass

        if KiemTraElementCoTonTaiKhong(adb_path, text=defined.searchbyEmailBtn):
            ClickVaoButtonTrungText(adb_path, defined.backBtn)
            pass
        else:
            pass
        time.sleep(1)

        if ClickVaoButtonTrungText(adb_path, defined.signupWithEmailBtn):
            pass
        
        # if DoiElementLoad(adb_path, defined.signupWithPhoneBtn):
        #     pass

        emailText = ["daylamaitest@gmail.com"]
        ToaDoField = XacDinhLoaiField(adb_path, "EditText")
        if NhapTextVaoField(adb_path, ToaDoField, emailText):
            DoiElementLoad(adb_path, defined.nextBtn)
            pass

        if KiemTraElementCoTonTaiKhong(adb_path, text=defined.showPassWordBtn):
            pass

        passText = ["daylapassconcu"]
        ToaDoField = XacDinhLoaiField(adb_path, "EditText")
        if NhapTextVaoField(adb_path, ToaDoField, passText):
            DoiElementLoad(adb_path, defined.nextBtn)
            pass

        if DoiElementLoad(adb_path, defined.notnowBtn):
            pass

        if DoiElementLoad(adb_path, defined.iagreeBtn):
            pass

        print("Đã hoàn thành việc nhập dữ liệu test!")

    except Exception as e:
        print(f"Không thể cài đặt APK hoặc nhập dữ liệu test. Lỗi: {e}")

# Gọi hàm với đường dẫn tới APK
apk_path = os.getenv('APK_PATH')  # Đổi đường dẫn tới APK bạn muốn cài
open_bluestacks_and_install_apk(apk_path)