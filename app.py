import os
import subprocess
import time
import random
import requests
from dotenv import load_dotenv
from include.detectButton import ClickVaoButtonTrungText, DoiElementLoad, ClickVaoClassName
from include.detectFields import XacDinhLoaiField, NhapTextVaoField
from include.detectNumPicker import ChonNgayThangNamSinh
from validate.validate import KiemTraElementCoTonTaiKhong, KiemTraClassCoTonTai

load_dotenv()

bluestacks_path = os.getenv('BLUESTACKS_PATH')
adb_path = os.getenv('ADB_PATH')
package_name = os.getenv('PACKAGE_NAME')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')

def OpenToolRegFaceBook(adb_path, defined):
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